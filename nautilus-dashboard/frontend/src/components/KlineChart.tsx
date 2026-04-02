// frontend/src/components/KlineChart.tsx
import React, { useEffect, useRef, useState } from 'react';
import * as echarts from 'echarts';

const KlineChart: React.FC = () => {
  const [data, setData] = useState<any[]>([]);
  const chartRef = useRef<HTMLDivElement | null>(null);
  const chartInstance = useRef<any>(null);

  useEffect(() => {
    // 从后端获取K线数据
    fetch('http://localhost:8000/api/klines?limit=200')
      .then(res => res.json())
      .then(d => setData(d.data))
      .catch(err => console.error('Failed to fetch klines:', err));
  }, []);

  // 初始化图表
  useEffect(() => {
    if (!chartRef.current) return;
    chartInstance.current = echarts.init(chartRef.current);

    const onResize = () => chartInstance.current && chartInstance.current.resize();
    window.addEventListener('resize', onResize);
    return () => {
      window.removeEventListener('resize', onResize);
      chartInstance.current && chartInstance.current.dispose();
    };
  }, []);

  // 渲染数据（K线 + 成交量 + dataZoom）
  useEffect(() => {
    if (!chartInstance.current || data.length === 0) return;

    const dates = data.map((k: any) => new Date(k.time).toLocaleDateString());
    const ohlc = data.map((k: any) => [k.open, k.close, k.low, k.high]);
    const volume = data.map((k: any) => k.volume);

    const option = {
      animation: false,
      legend: { data: ['Candlestick', 'Volume'] },
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'cross' },
      },
      grid: [{ left: '10%', right: '15%', height: '65%' }, { left: '10%', right: '15%', top: '75%', height: '18%' }],
      xAxis: [
        { type: 'category', data: dates, scale: true, boundaryGap: true, axisLine: { onZero: false }, splitLine: { show: false }, min: 'dataMin', max: 'dataMax' },
        { type: 'category', data: dates, gridIndex: 1, axisLabel: { show: false } },
      ],
      yAxis: [
        { scale: true, splitArea: { show: false } },
        { gridIndex: 1, splitNumber: 3, axisLabel: { show: true } },
      ],
      dataZoom: [
        { type: 'inside', xAxisIndex: [0, 1], start: 50, end: 100 },
        { show: true, xAxisIndex: [0, 1], type: 'slider', top: '90%', start: 50, end: 100 },
      ],
      series: [
        {
          name: 'Candlestick',
          type: 'candlestick',
          data: ohlc,
          itemStyle: { color: '#ec0000', color0: '#00da3c', borderColor: '#8A0000', borderColor0: '#008F28' },
        },
        {
          name: 'Volume',
          type: 'bar',
          xAxisIndex: 1,
          yAxisIndex: 1,
          data: volume,
          itemStyle: { color: '#7f8c8d' },
        },
      ],
    };

    chartInstance.current.setOption(option);
  }, [data]);

  // WebSocket 实时更新：接收trade并更新最后一根K线(close和volume)
  useEffect(() => {
    if (!chartInstance.current) return;
    const ws = new WebSocket('ws://localhost:8000/ws/trades');
    ws.onopen = () => console.log('WS connected');
    ws.onmessage = (ev) => {
      try {
        const msg = JSON.parse(ev.data);
        // msg: { timestamp, price, quantity, side }
        // 把trade合并到最后一根K线：更新 close 和 volume
        setData(prev => {
          if (!prev || prev.length === 0) return prev;
          const next = prev.slice();
          const last = { ...next[next.length - 1] };
          // 更新收盘价为trade价格
          last.close = Number(msg.price);
          // 调整高低
          last.high = Math.max(last.high, last.close);
          last.low = Math.min(last.low, last.close);
          // 增加成交量
          last.volume = Number(last.volume) + Number(msg.quantity);
          next[next.length - 1] = last;

          // 直接更新图表以减少延迟
          const dates = next.map((k: any) => new Date(k.time).toLocaleDateString());
          const ohlc = next.map((k: any) => [k.open, k.close, k.low, k.high]);
          const volume = next.map((k: any) => k.volume);
          chartInstance.current.setOption({
            xAxis: [{ data: dates }, { data: dates }],
            series: [{ data: ohlc }, { data: volume }],
          });

          return next;
        });
      } catch (e) {
        console.error('WS message parse error', e);
      }
    };
    ws.onclose = () => console.log('WS closed');
    ws.onerror = (e) => console.error('WS error', e);

    return () => ws.close();
  }, [chartInstance.current]);

  return <div ref={chartRef} style={{ width: '100%', height: '500px' }} />;
};

export default KlineChart;