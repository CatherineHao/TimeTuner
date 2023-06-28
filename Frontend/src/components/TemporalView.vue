<!--
 * @Description: 
 * @Author: Qing Shi
 * @Date: 2023-01-10 21:20:01
 * @LastEditTime: 2023-06-21 10:14:36
-->
<template>
    <div class="frameworkTitle" style="padding-right: 10px;">
        <div class="title">Temporal View</div>
        <p class="titleTriangle"></p>
        <div style="float: right; margin-top: 3px;">
            <span>Metric: </span>
            <el-select v-model="heatTag" class="m-2" placeholder="Select" style="width: 150px;">
                <el-option v-for="(item, i) in heatOptions" :key="item" :label="item" :value="i" />
            </el-select>
        </div>
    </div>
    <div class="frameworkBody">
    
        <div ref="timeline" style="height: calc(100%); width: 100%; margin-top: 0px;">
            <svg id="timeline" height="100%" width="100%">
                            <g :transform="translate(0, 0, 0)" id="timeline_g">
                                <g id="raw_line_g" :transform="translate(0, 0, 0)">
                                        <defs>
                                            <clipPath id="clipPath">
                                                <rect :x="50" :y="20" :width="tlWidth - 70" :height="tlHeight - 50"></rect>
                                        </clipPath>
                                    </defs>
                                    <g id="brush_path_g" clip-path="url(#clipPath)">
                                    </g>
                                        <g>
                                            <path :d="smoothTimeLineData" stroke="red" :fill="'none'"></path>
                                    </g>
                                </g>
                                <g :transform="translate(0, tlHeight - 100 - 30, 0)" id="focusLine_g">
                                    <path :d="brushTimeLineData" stroke="#777" :fill="'none'"></path>
                                    <g id="brush_path_line"></g>
                                    </g>
                
                                <g id="brush_g" :transform="translate(0, tlHeight - 100 - 30, 0)"></g>
                            </g>
                        </svg>
        </div>
    
    </div>
</template>

<script>
import res_data from '../assets/model_skip_results.json';

import { arc, curveBumpY, line } from 'd3-shape';
import { scaleUtc, scaleLinear, scaleOrdinal } from 'd3-scale';
import { axisLeft, axisBottom } from 'd3-axis';
import { interpolateRdBu, interpolateYlOrRd, schemeYlOrRd } from 'd3-scale-chromatic';
import { useDataStore } from "../stores/counter";
import SN_raw_data from "../assets/SN_m_tot_V2.0.csv";

import { select, selectAll } from 'd3-selection';
import { extent, max, min, sum } from 'd3-array';
import { brushX } from 'd3-brush';
import * as vsup from 'vsup';
export default {
    name: 'DataTransformationView',
    props: ['timeData', 'sliceData'],
    data() {
        return {
            elHeight: 1000,
            elWidth: 1000,
            tlHeight: 100,
            tlWidth: 100,
            heatHeight: 0,
            heatTag: 3,
            timeBrush: null,
            allTimeScale: null,
            heatOptions: ['Raw + Difference', 'Raw', 'Difference', 'RMSE + Corr.', 'RMSE', 'Corr.'],
            sample: ['10-slice', '7-slice', '3-slice'],
            smooth: ['Raw Sequence', 'N-Average', 'EMA/Holt'],
            d: [],
            startTime: 0,
            timeScale: null,
            maeScale: null,
            timeSliceData: [],
            barData: [],
            tableData: [],
            rawTimeLineData: 'M 0 0',
            brushTimeLineData: 'M 0 0',
            smoothTimeLineData: 'M 0 0',
            timeAxis: [],
            brushTimeAxis: [],
            sparkboxData: [],
            heatRectData: [],
            selectAverageLine: [],
            scaleRange: {
                raw: [99999, -999999],
                error: [99999, -999999]
            },
            groupPath: [],
            smoothData: [],
            select_smooth_data: [],
            select_time_step: [0, 2459],
            lineGenerateFunc: null,
            yScale: null,
            xScale: null,
            rxScale: null,
            lineData: [],
            smoothLineData: [],
            skip_length: [13, 1, 3, 6, 13, 1, 3, 6, 13, 1, 3, 6, 13, 1, 3, 6, 13, 1, 3, 6, 13, 1, 3, 6, 13, 1, 3, 6, 13, 1, 3, 6, 13, 1, 3, 6],
            columnData: ['Smooth', 'Skip', 'Train-Loss', 'Test-Loss', 'ACF', 'Window Performance'],
            filename: ['rawdata_skip13_0.8.csv',
                'rawdata_skip1_0.8.csv',
                'rawdata_skip3_0.8.csv',
                'rawdata_skip6_0.8.csv',
                'rolling13_skip13_0.8.csv',
                'rolling13_skip1_0.8.csv',
                'rolling13_skip3_0.8.csv',
                'rolling13_skip6_0.8.csv',
                'rolling3_skip13_0.8.csv',
                'rolling3_skip1_0.8.csv',
                'rolling3_skip3_0.8.csv',
                'rolling3_skip6_0.8.csv',
                'rolling6_skip13_0.8.csv',
                'rolling6_skip1_0.8.csv',
                'rolling6_skip3_0.8.csv',
                'rolling6_skip6_0.8.csv',
                'rolling9_skip13_0.8.csv',
                'rolling9_skip1_0.8.csv',
                'rolling9_skip3_0.8.csv',
                'rolling9_skip6_0.8.csv',
                'weighted13_skip13_0.8.csv',
                'weighted13_skip1_0.8.csv',
                'weighted13_skip3_0.8.csv',
                'weighted13_skip6_0.8.csv',
                'weighted3_skip13_0.8.csv',
                'weighted3_skip1_0.8.csv',
                'weighted3_skip3_0.8.csv',
                'weighted3_skip6_0.8.csv',
                'weighted6_skip13_0.8.csv',
                'weighted6_skip1_0.8.csv',
                'weighted6_skip3_0.8.csv',
                'weighted6_skip6_0.8.csv',
                'weighted9_skip13_0.8.csv',
                'weighted9_skip1_0.8.csv',
                'weighted9_skip3_0.8.csv',
                'weighted9_skip6_0.8.csv'
            ],
            filename_type: ['RAW_13',
                'RAW_1',
                'RAW_3',
                'RAW_6',
                'MA-13_13',
                'MA-13_1',
                'MA-13_3',
                'MA-13_6',
                'MA-3_13',
                'MA-3_1',
                'MA-3_3',
                'MA-3_6',
                'MA-6_13',
                'MA-6_1',
                'MA-6_3',
                'MA-6_6',
                'MA-9_13',
                'MA-9_1',
                'MA-9_3',
                'MA-9_6',
                'WMA-13_13',
                'WMA-13_1',
                'WMA-13_3',
                'WMA-13_6',
                'WMA-3_13',
                'WMA-3_1',
                'WMA-3_3',
                'WMA-3_6',
                'WMA-6_13',
                'WMA-6_1',
                'WMA-6_3',
                'WMA-6_6',
                'WMA-9_3',
                'WMA-9_13',
                'WMA-9_1',
                'WMA-9_6'
            ],
            smoothTag: 0,
            timeLinePath: null,
            linePathTag: 0,
            coverRect: [],
            predict_line: [],
            predict_tag: 0
        }
    },
    methods: {
        selectFile(num) {

            select('#rst' + num).attr('stroke-width', 3)
            // .attr('fill', '#777').attr('fill-opacity', 0.5);
            selectAll('.p_x').attr('opacity', (d, i) => {
                return d.id == num ? 1 : 0;
            })
        },
        clickFile(num) {
            let tdata = []
            selectAll('.corr_cir').attr('opacity', (d, i) => {
                if (d.class_name == this.filename[num].substring(0, this.filename[num].length - 8)) {
                    tdata.push(d);
                    // return 0.5;
                }
                return d.isShow ? 0 : 0.5;
            }).attr('fill', (d, i) => {
                // if (d.class_name == this.filename[num].substring(0, this.filename[num].length - 8)) return 'orange';
                // else 
                return '#d9d9d9';
            })
            // console.log(tdata)
            selectAll('.corr_cir_out').remove();
            select('#scatter')
                .append('g')
                .selectAll('#res_c')
                .attr('id', 'res_c')
                .data(tdata)
                .enter()
                .append('circle')
                .attr('cx', d => d.x)
                .attr('cy', d => d.y)
                .attr('id', (d, i) => 'corr_c' + d.id_cnt)
                .attr('class', 'corr_cir_out')
                .attr('r', 3)
                .attr('stroke', 'black')
                .attr('fill', d => d.fill)
        },
        cancelFile(num) {
            select('#rst' + num).attr('stroke-width', 0);
            selectAll('.p_x').attr('opacity', 1)
            // selectAll('.corr_cir').attr('opacity', (d, i) => {
            //     // if (d.class_name == this.filename[num].substring(0, this.filename[num].length - 8)) {
            //     //     return 1;
            //     // }
            //     return 1;
            // })
        },
        colorScale: function(raw_value, error_value, tag) {
            let rawRange = this.scaleRange.raw;
            let errorRange = this.scaleRange.error;

            let heatColor = interpolateYlOrRd;
            // let heatColor = interpolateRdBu;
            let rawDataScale = scaleLinear(rawRange, [0, 1]);
            let errorDataScale = scaleLinear(errorRange, [0, 1]);
            let quantization = vsup.quantization().branching(2).layers(4).valueDomain(rawRange).uncertaintyDomain(errorRange);
            let heatScale = vsup.scale().quantize(quantization).range(heatColor);

            if (tag == "Raw + RMSE") {
                return heatScale(raw_value, error_value);
            } else if (tag == "Raw") {
                return heatColor(rawDataScale(raw_value, error_value));
            } else if (tag == "RMSE") {
                return heatColor(errorDataScale(raw_value, error_value));
            }
        },
        translate(x, y, deg) {
            return `translate(${x}, ${y}) rotate(${deg})`;
        },
        calcCurve() {
            let p1 = [
                [this.elWidth / 2, 75],
                [this.elWidth / 2 - this.elWidth / 3, 75 + (this.elHeight - 75 * 3) / 2]
            ];
            let p2 = [
                [this.elWidth / 2, 75],
                [this.elWidth / 2 + this.elWidth / 3, 75 + (this.elHeight - 75 * 3) / 2]
            ];
            let p3 = [
                [this.elWidth / 2 - this.elWidth / 3, -((this.elHeight - 75 * 3) / 2)],
                [(this.elWidth - 40) / 18, 0]
            ];
            let p4 = [
                [this.elWidth / 2 - this.elWidth / 3, -(this.elHeight - 75 * 3) / 2],
                [2 * (this.elWidth - 40) / 9 + (this.elWidth - 40) / 18 + 10, 0]
            ];
            let cline = line().curve(curveBumpY);
            let d = [cline(p1), cline(p2), cline(p3), cline(p4)];
            return d;
        },
        calcSparkBox(data, height, width) {
            let margin = ({ top: 20, right: 20, bottom: 30, left: 50 });
            // let height = 440;
            // let width = 1000;
            let focusHeight = 100;

            let y = scaleLinear()
                .domain([0, max(data, d => parseFloat(d.value))])
                .range([height - focusHeight - 30 - margin.bottom, margin.top])
            let sBData = [];
            let y2 = scaleLinear()
                .domain([0, max(data, d => parseFloat(d.value))])
                .range([focusHeight, margin.top])
            // let x = scaleLinear()
            //     .domain([0, max(data, d => parseInt(d.id))])
            //     .range([margin.left, width - margin.right])
            let x = this.xScale;
            let sparkBoxData = [];
            let timeGap = 130
            for (let i = 0; i < data.length; i += timeGap) {
                // let tempValue = Array.from(new Set(data.slice(i, i + 10).map(d => parseFloat(d.value)).sort((a, b) => a - b)));
                let tempValue = data.slice(i, i + timeGap).map(d => parseFloat(d.value)).sort((a, b) => a - b)
                let sumData = sum(tempValue);

                // console.log(sumData)

                // console.log(tempValue[tempValue.length /2 - 1], tempValue.length /2 - 1);
                sBData.push({
                    x: x(parseInt(data[i].id)),
                    y: y(tempValue[tempValue.length - 1]),
                    w: Math.abs(x(parseInt(data[i + ((i + timeGap < data.length) ? timeGap : (data.length - 1 - i))].id)) - x(parseInt(data[i].id))),
                    h: Math.abs(y(tempValue[0]) - y(tempValue[tempValue.length - 1]))
                })
                sBData.push({
                    x: x(parseInt(data[i].id)),
                    y: y(tempValue[parseInt(tempValue.length * 3 / 4) - 1]),
                    w: Math.abs(x(parseInt(data[i + ((i + timeGap < data.length) ? timeGap : (data.length - 1 - i))].id)) - x(parseInt(data[i].id))),
                    h: Math.abs(y(tempValue[parseInt(tempValue.length * 3 / 4) - 1]) - y(tempValue[parseInt(tempValue.length / 4) - 1]))
                })
                sBData.push({
                    x: x(parseInt(data[i].id)),
                    // y: y(tempValue[parseInt(tempValue.length /2) - 1]),
                    // y: y((tempValue[0] + tempValue[parseInt(tempValue.length - 1)]) / 2),
                    y: y(sumData / tempValue.length),
                    w: Math.abs(x(parseInt(data[i + ((i + timeGap < data.length) ? timeGap : (data.length - 1 - i))].id)) - x(parseInt(data[i].id))),
                    h: 1
                })
                sparkBoxData.push({
                    rect1: {
                        x: x(parseInt(data[i].id)),
                        y: y(tempValue[tempValue.length - 1]),
                        w: Math.abs(x(parseInt(data[i + ((i + 10 < data.length) ? 10 : (data.length - 1 - i))].id)) - x(parseInt(data[i].id))),
                        h: Math.abs(y(tempValue[0]) - y(tempValue[tempValue.length - 1]))
                    },
                    rect2: {
                        x: x(parseInt(data[i].id)),
                        y: y(tempValue[parseInt(tempValue.length * 3 / 4) - 1]),
                        w: Math.abs(x(parseInt(data[i + ((i + 10 < data.length) ? 10 : (data.length - 1 - i))].id)) - x(parseInt(data[i].id))),
                        h: Math.abs(y(tempValue[parseInt(tempValue.length * 3 / 4) - 1]) - y(tempValue[parseInt(tempValue.length / 4) - 1]))
                    },
                    line: {
                        x1: x(parseInt(data[i].id)),
                        // y: y(tempValue[parseInt(tempValue.length /2) - 1]),
                        // y: y((tempValue[0] + tempValue[parseInt(tempValue.length - 1)]) / 2),
                        y: y(sumData / tempValue.length),
                        x2: Math.abs(x(parseInt(data[i + ((i + 10 < data.length) ? 10 : (data.length - 1 - i))].id)) - x(parseInt(data[i].id))) + x(parseInt(data[i].id))
                    }
                })
            }
            selectAll('.sparkbox').remove();
            selectAll('#time_path_raw').remove();
            select('#brush_path_g').append('g').attr('class', 'sparkbox').selectAll('#sparkRect').attr('id', 'sparkRect').data(sBData).enter().append('rect').attr('x', d => d.x).attr('y', d => d.y).attr('width', d => d.w).attr('height', d => d.h).attr('fill', (d, i) => {
                if (i % 3 == 0) {
                    return '#f2f5fa';
                } else if (i % 3 == 1) {
                    return '#dce3f3'
                } else return '#6d70b6';
            });
            select('#brush_path_g')
                // .append('g')
                // .data([{
                //     value: data
                // }])
                // .enter()
                .append('path')
                .attr('id', 'time_path_raw')
                .attr('d', d => {
                    return this.timeLinePath
                })
                .attr('stroke', '#777')
                .attr('stroke-width', 1.5)
                .attr('fill', 'none')
                .style('z-index', 5)

            // console.log(sparkboxData)
            // return sparkboxData;
        },
        setupBrush: function(data) {
            let width = this.tlWidth;
            let height = this.tlHeight;
            let focusHeight = 100;
            let margin = ({ top: 20, right: 20, bottom: 30, left: 50 });
            const timeBrush = brushX()
                .extent([
                    [margin.left, margin.top],
                    [width - margin.right, focusHeight]
                ])
                .on('start', brushStart)
                .on('brush', brushed)
                .on('end', brushEnd);
            this.timeBrush = timeBrush;
            let x = scaleLinear()
                .domain([0, max(data, d => parseInt(d.id))])
                .range([margin.left, width - margin.right])
            this.allTimeScale = x;

            let _this = this;
            let radius = focusHeight / 2 - 10;
            let arcA = arc()
                .innerRadius(0)
                .outerRadius(radius)
                .startAngle(0)
                .endAngle((d, i) => i ? Math.PI : -Math.PI)
            let brushHandle = (g, s) => g
                .selectAll(".handle--custom")
                .data([{ type: "w" }, { type: "e" }])
                .join(
                    enter => enter.append("path")
                    .attr("class", "handle--custom")
                    .attr("fill", "white")
                    .attr("opacity", 1)
                    .attr("stroke", "#777")
                    .attr("stroke-width", 1)
                    .attr("cursor", "ew-resize")
                    .attr("d", 'M -5 ' + (-focusHeight / 2 + 30) + ' L -5 ' + (focusHeight / 2 - 30) + 'L 5 ' + (focusHeight / 2 - 30) + ' L 5 ' + (-focusHeight / 2 + 30) + ' Z'),
                )
                .attr("display", s === null ? "none" : null)
                .attr("transform", s === null ? null : (d, i) => `translate(${s[i]},${radius + margin.top})`)

            function brushStart() {
                selectAll('.sparkbox').remove();
            }

            function brushEnd({ selection }) {
                _this.calcSparkBox(SN_raw_data, _this.tlHeight, _this.tlWidth);
                let timeStep = [parseInt(_this.rxScale(selection[0])), parseInt(_this.rxScale(selection[1]))];
                // let maxY = max(data, (d, i) => {
                //     if (i >= timeStep[0] && i <= timeStep[1]) {
                //     return parseFloat(d.value)
                //     }
                //     return 0;
                // });


                _this.xScale.domain(timeStep);
                // _this.yScale.domain([0, maxY]);
                let xAxis = [];
                let timeRange = [];
                let lenRange = [];
                let cnt_i = 0
                for (let ii = timeStep[0]; ii <= timeStep[1]; ii += Math.floor(timeStep[1] - timeStep[0]) / 10) {
                    // console.log(i, _this.lineData);
                    let i = parseInt(ii);
                    cnt_i = i;
                    xAxis.push({
                        x: _this.xScale(i),
                        y: 0,
                        // text: parseInt(parseInt(_this.lineData[i].timestamp) / 100) + '.' + parseInt(parseInt(_this.lineData[i].timestamp) % 100)
                        text: (_this.lineData[i].timestamp)
                    });
                    timeRange.push(_this.lineData[i].timestamp);
                    lenRange.push(_this.xScale(i))
                }
                if (timeRange.length == 10) {
                    timeRange.push('');
                    lenRange.push(_this.elWidth - 20)
                }
                let tScale = scaleOrdinal(timeRange, lenRange)
                // console.log(timeRange, lenRange);
                selectAll('#axsg').remove();
                select('#focusLine_g').append('g').attr('id', 'axsg').attr("transform", `translate(0, ${-30})`).call(axisBottom(tScale));

                // _this.timeAxis = xAxis;

                let lineGenerate = line()
                    .x(d => _this.xScale(d.id))
                    .y(d => _this.yScale(d.value));

                _this.select_time_step = timeStep;

                select('#time_path_raw').attr('d', lineGenerate(_this.lineData));
                if (_this.smoothTag) {

                    select('#time_path_selected').attr('d', lineGenerate(_this.smoothLineData));
                }
            }

            function brushed({ selection }) {
                // console.log(selection);
                let timeStep = [parseInt(_this.rxScale(selection[0])), parseInt(_this.rxScale(selection[1]))];
                _this.xScale.domain(timeStep);
                // _this.yScale.domain([0, maxY]);
                let xAxis = [];
                let timeRange = [];
                let lenRange = [];
                let cnt_i = 0
            // select("#timeline_g").append('path').attr('id', 'selected_area').attr('d', 'M ' + parseInt(988) + ' ' + 85 + ' L ' + parseInt(1760) + ' ' + 85 + ' L ' + (_this.elWidth) + ' 130 L 50 130 Z').attr('stroke', '#777').attr('stroke-width', 1).attr('fill', '#777').attr('opacity', 0.15);    
                for (let ii = timeStep[0]; ii <= timeStep[1]; ii += Math.floor(timeStep[1] - timeStep[0]) / 10) {
                    // console.log(i, _this.lineData);
                    let i = parseInt(ii);
                    cnt_i = i;
                    xAxis.push({
                        x: _this.xScale(i),
                        y: 0,
                        // text: parseInt(parseInt(_this.lineData[i].timestamp) / 100) + '.' + parseInt(parseInt(_this.lineData[i].timestamp) % 100)
                        text: (_this.lineData[i].timestamp)
                    });
                    timeRange.push(_this.lineData[i].timestamp);
                    lenRange.push(_this.xScale(i))
                }
                if (timeRange.length == 10) {
                    timeRange.push('');
                    lenRange.push(_this.elWidth - 20)
                }
                let tScale = scaleOrdinal(timeRange, lenRange)
                // console.log(timeRange, lenRange);
                selectAll('#axsg').remove();
                select('#focusLine_g').append('g').attr('id', 'axsg').attr("transform", "translate(0, -25)").call(axisBottom(tScale));

                // _this.timeAxis = xAxis;

                let lineGenerate = line()
                    .x(d => _this.xScale(d.id))
                    .y(d => _this.yScale(d.value));

                _this.select_time_step = timeStep;

                select('#time_path_raw').attr('d', lineGenerate(_this.lineData));
                if (_this.predict_tag) {

                    select('#sel_predict_line').attr('d', lineGenerate(_this.predict_line));
                }

                select("#selected_area").attr('d', 'M ' + parseInt(selection[0]) + ' ' + 441 + ' L ' + parseInt(selection[1]) + ' ' + 441 + ' L ' + (_this.tlWidth - margin.right) + ' 393 L 50 393 Z')
                select(this).call(brushHandle, selection);

                // console.log(timeStep);
                // _this.calcTimeLineCompare(data, [], _this.tlHeight, _this.tlWidth, _this.select_time_step)
                // let d = _this.calcTimeLineCompare(SN_raw_data, [], _this.tlHeight, _this.tlWidth, _this.select_time_step);

                // _this.rawTimeLineData = d[0];
                // _this.smoothTimeLineData = d[1];
            }
            select('#brush_g').call(timeBrush)
                .call(timeBrush.move, [x(988), x(1760)]);

        },
        calcOverviewTimeLine(data) {
            
        },
        calcTimeLine(data, height, width) {
            let margin = ({ top: 20, right: 20, bottom: 30, left: 50 });
            // let height = 440;
            // let width = 1000;
            let focusHeight = 100;

            let y = scaleLinear()
                .domain([0, max(data, d => parseFloat(d.value))])
                .range([height - focusHeight - 30 - margin.bottom, margin.top])
            let y2 = scaleLinear()
                .domain([0, max(data, d => parseFloat(d.value))])
                .range([focusHeight, margin.top])
            let x = scaleLinear()
                .domain([0, max(data, d => parseInt(d.id))])
                .range([margin.left, width - margin.right])
            const rx = scaleLinear()
                .domain([margin.left, width - margin.right])
                .range([0, max(data, d => parseInt(d.id))]);

            let timeData = [];
            let lenData = [];
            for (let i = 0; i < data.length; ++i) {

                if (i == 0 || i == data.length - 1 || i % Math.floor(data.length / 10) === 0) {
                    lenData.push(x(parseInt(data[i].id)));
                    timeData.push(parseInt(data[i].timestamp));
                }
            }
            let timeScale = scaleOrdinal(timeData, lenData);
            select('#focusLine_g').append('g').call(axisBottom(timeScale).tickSizeOuter(0).tickPadding(10)).attr('transform', `translate(0,${focusHeight})`).call(g => g.selectAll(".title").data(['Time']).join("text")
                .attr("class", "title")
                .attr("x", this.elWidth - 20)
                .attr("y", 35)
                .attr("fill", "currentColor")
                .attr("text-anchor", "middle")
                .attr('font-size', '14px')
                .text(''))
            this.xScale = x;
            this.yScale = y;
            this.rxScale = rx;
            // console.log(y.domain(), x.domain(), data);

            // let area = (x, y) => d3.area()
            //     .defined(d => !isNaN(d.value))
            //     .x(d => x(d.date))
            //     .y0(y(0))
            //     .y1(d => y(d.value))
            let lineGenerate = line()
                .x(d => x(d.id))
                .y(d => y(d.value));
            this.lineGenerateFunc = lineGenerate;

            let lineGenerate2 = line()
                .x(d => x(d.id))
                .y(d => y2(d.value));

            let yAxis = (g, y, title) => g
                .attr("transform", `translate(${margin.left},${0})`)
                .call(axisLeft(y))
                // .call(g => g.select(".domain").remove())
                .call(g => g.selectAll(".title").data([title]).join("text")
                    .attr("class", "title")
                    .attr("x", 0)
                    .attr("y", 12)
                    .attr("fill", "currentColor")
                    .attr("text-anchor", "middle")
                    .attr('font-size', '14px')
                    .text(title));
            let xAxis = (g, x, height) => g
                .attr("transform", `translate(0,${height - margin.bottom})`)
                .call(axisBottom(x).ticks(width / 80).tickSizeOuter(0));
            let timeAxis = []
            for (let i = 0; i < data.length; i += parseInt(data.length / 10)) {
                timeAxis.push({
                    x: x(i),
                    text: parseInt(parseInt(data[i].timestamp) / 100) + '.' + parseInt(parseInt(data[i].timestamp) % 100)
                })
            }
            this.timeAxis = timeAxis;
            this.brushTimeAxis = timeAxis;
            // select('#timeline').append('g').call(xAxis, x, focusHeight);
            select('#raw_line_g').append('g').attr('id', 'yAxis_g').call(yAxis, y, 'Value');
            // select('#brush_path_g').append("defs").append("clipPath")
            //     .attr("id", "clip")
            //     .append("rect")
            //     .attr('x', margin.left)
            //     .attr('y', margin.top)
            //     .attr("width", width - margin.right - margin.left)
            //     .attr("height", height - 100 - margin.bottom - margin.top);
            // select('#brush_path_g')
            //     // .append('g')
            //     // .data([{
            //     //     value: data
            //     // }])
            //     // .enter()
            //     .append('path')
            //     .attr('id', 'time_path_raw')
            //     .attr('d', d => {
            //         return lineGenerate(data)
            //     })
            //     .attr('stroke', '#777')
            //     .attr('stroke-width', 1.5)
            //     .attr('fill', 'none')
            //     .style('z-index', 5)
            this.timeLinePath = lineGenerate(data);
            const _this = this;



            select('#brush_path_line')
                // .append('g')
                // .data([{
                //     value: data
                // }])
                // .enter()
                .append('path')
                .attr('id', 'time_brush')
                .attr('d', d => {
                    return lineGenerate2(data)
                })
                .attr('stroke', '#777')
                .attr('stroke-width', 1)
                .attr('fill', 'none')
            this.lineData = data;

            // return [lineGenerate(data), lineGenerate2(data)];
        },
        calcTimeLineCompare(tsmooth_data) {
            this.smoothTag = 1;
            this.smoothLineData = tsmooth_data;

            let lineGenerate = line()
                .x(d => this.xScale(d.id))
                .y(d => this.yScale(d.value));
            select('#brush_path_g')
                // .append('g')
                // .data([{
                //     value: data
                // }])
                // .enter()
                .append('path')
                .attr('id', 'time_path_selected')
                .attr('d', d => {
                    return lineGenerate(tsmooth_data)
                })
                .attr('stroke', 'red')
                .attr('stroke-width', 1.5)
                .attr('fill', 'none')
            // return [lineGenerate(data), lineGenerate(smooth_data), average_line];
        },
        timeCompare(select_num) {
            // console.log(select_num, this.smoothData);
            this.select_smooth_data = this.smoothData[select_num]
            this.calcTimeLineCompare(this.smoothData[select_num]);

            // this.rawTimeLineData = d[0];
            // this.smoothTimeLineData = d[1];
            // console.log(d[1], this.smoothTimeLineData);
        },
        calcMonth(startTime, endTime) {
            let year = parseInt(endTime / 100) - parseInt(startTime / 100);
            let month = endTime % 100 - startTime % 100 + 1;
            let sumMonth = year * 12 + month;
            return sumMonth;
        },
        calcHeat(raw_data, smooth_data, skipLength, width, tag) {
            let margin = ({ top: 20, right: 50, bottom: 30, left: 50 });
            let x = scaleLinear()
                .domain([0, max(raw_data, d => parseInt(d.id))])
                .range([margin.left, width - margin.right])
            let heat_data = [];
            for (let i = 0; i < raw_data.length; i += skipLength) {
                // let tempValue = Array.from(new Set(data.slice(i, i + 10).map(d => parseFloat(d.value)).sort((a, b) => a - b)));
                let rawTempValue = raw_data.slice(i, i + skipLength).map(d => parseFloat(d.value)).sort((a, b) => a - b)
                let rawSum = sum(rawTempValue);
                let smoothTempValue = smooth_data.slice(i, i + skipLength).map(d => parseFloat(d.value)).sort((a, b) => a - b)
                let smoothSum = sum(smoothTempValue);
                heat_data.push({
                    rawData: smoothSum / smoothTempValue.length,
                    errorData: Math.abs(rawSum / rawTempValue.length - smoothSum / smoothTempValue.length),
                    x: x(parseInt(raw_data[i].id)),
                    w: Math.abs(x(parseInt(raw_data[i + ((i + skipLength < raw_data.length) ? skipLength : (raw_data.length - 1 - i))].id)) - x(parseInt(raw_data[i].id))),
                });
            }
            let rawRange = [min(heat_data, d => d.rawData), max(heat_data, d => d.rawData)];
            let errorRange = [min(heat_data, d => d.errorData), max(heat_data, d => d.errorData)];
            // console.log(rawRange, errorRange)
            let heatRectData = [];
            let rawRectData = [];
            let errorRectData = [];
            let heatColor = interpolateYlOrRd;
            // let heatColor = interpolateRdBu;
            let rawDataScale = scaleLinear(rawRange, [0, 1]);
            let errorDataScale = scaleLinear(errorRange, [0, 1]);
            // let heatScale = scaleLinear([0, 14], [0, 1]);
            // let colorStep = [1, 2, 4, 8];

            let quantization = vsup.quantization().branching(2).layers(4).valueDomain(rawRange).uncertaintyDomain(errorRange);
            let heatScale = vsup.scale().quantize(quantization).range(heatColor);
            for (let i in heat_data) {
                let hd = heat_data[i];
                // let errorScale = parseFloat((hd.errorRange - errorRange[0]) / (errorRange[1] - errorRange[0]));
                // let errorStep = ((errorScale * 4 == parseInt(errorScale * 4)) && errorScale != 0) ? parseInt(errorScale * 4) - 1 : parseInt(errorScale * 4);
                // let rawScale = parseFloat((hd.rawData - rawRange[0]) / (rawRange[1] - rawRange[0]));
                // // console.log(parseInt(rawScale * 4))
                // let colorScale = sum(colorStep.slice(0, errorStep)) + parseInt(rawScale * colorStep[errorStep]);
                // console.log(colorScale,colorStep[errorStep], errorStep, sum(colorStep.slice(0, parseInt(errorScale * 4))))
                this.scaleRange.raw[0] = Math.min(this.scaleRange.raw[0], hd.rawData);
                this.scaleRange.raw[1] = Math.max(this.scaleRange.raw[1], hd.rawData);
                this.scaleRange.error[0] = Math.min(this.scaleRange.error[0], hd.rawData);
                this.scaleRange.error[1] = Math.max(this.scaleRange.error[1], hd.rawData);

                heatRectData.push({
                    t: tag,
                    x: hd.x,
                    w: hd.w,
                    h: this.elHeight / 22 - 3,
                    // color: (heatScale(hd.rawData, hd.errorData))
                    raw: hd.rawData,
                    error: hd.errorData
                });
                rawRectData.push({
                    t: tag,
                    x: hd.x,
                    w: hd.w,
                    h: this.elHeight / 22 - 3,
                    // color: heatColor(rawDataScale(hd.rawData))
                    raw: hd.rawData,
                    error: hd.errorData

                });
                errorRectData.push({
                    t: tag,
                    x: hd.x,
                    w: hd.w,
                    h: this.elHeight / 22 - 3,
                    // color: heatColor(errorDataScale(hd.errorData))
                    raw: hd.rawData,
                    error: hd.errorData
                });
                // console.log(heatColor(heatScale((colorScale != 0 ? colorScale - 1 : 0))), colorScale, heatScale((colorScale == 0 ? colorScale - 1 : 0)))
            }
            if (tag == 'raw')
                return {
                    heat: rawRectData,
                    raw: rawRectData,
                    error: rawRectData,
                    tag: tag,
                    h: this.elHeight / 22
                }
            return {
                heat: heatRectData,
                raw: rawRectData,
                error: errorRectData,
                tag: tag,
                h: this.elHeight / 22
            };
        },
        calcTimeScale(data) {
            let startTime = 9999999;
            let endTime = 0;
            let maeMax = 0;
            for (const d of data) {
                for (const sub_d of d['sub slice']) {
                    startTime = Math.min(startTime, parseInt(sub_d['train_begin']));
                    endTime = Math.max(endTime, parseInt(sub_d['test_end']));
                    maeMax = Math.max(maeMax, d['MAE']);
                }
            }
            let month = this.calcMonth(startTime, endTime);
            return [startTime, scaleLinear([0, month], [0, this.elWidth - 300]), scaleLinear([0, maeMax], [1, 0])];
        },
        calcTimeData(data) {
            let r_data = new Array();
            let t_data = new Object();
            let cnt = 0;
            // console.log(data['sub slice']);
            let maeRange = [min(data['sub slice'], d => d['MAE']), max(data['sub slice'], d => d['MAE'])];
            let maeScale = scaleLinear(maeRange, [0, 1]);


            for (const d of data['sub slice']) {
                r_data.push({
                    id: cnt++,
                    startTime: d['train_begin'],
                    endTime: d['test_end'],
                    train: {
                        x: this.timeScale(this.calcMonth(this.startTime, d['train_begin'])),
                        w: this.timeScale(this.calcMonth(d['train_begin'], d['train_end'])),
                        fill: '#777'
                    },
                    test: {
                        x1: this.timeScale(this.calcMonth(this.startTime, d['test_begin'])),
                        x2: this.timeScale(this.calcMonth(this.startTime, d['test_end'])),
                        w: this.timeScale(this.calcMonth(d['test_begin'], d['test_end'])),
                        fill: interpolateRdBu(maeScale(d['MAE']))
                    }
                })
            }

            let h_data = new Array();
            for (let i = 0; i < 20; ++i) {
                h_data.push({
                    fill: interpolateRdBu(Math.random())
                })
            }
            t_data = {
                slice: data['slice_info']['slice_number'] + '-slice',
                smooth: '13-Average',
                slice_num: parseInt(data['slice_info']['slice_number']),
                heat_data: h_data,
                // bar_data: r_data.reverse(),
                bar_data: r_data
            }
            return t_data;
        },
        calcGroup: function() {
            let midDot = (this.elHeight / 18);
            let left = 50;
            let groupRow = [];
            let groupColum = [];
            let tp = [];
            for (let i = 1; i <= 18; ++i) {
                groupRow.push({
                    x1: 50,
                    y1: (i) * midDot - this.elHeight / 36,
                    x2: 50 - 48 / 3,
                    y2: (i) * midDot - this.elHeight / 36
                });
                if (i % 2 == 0) {
                    groupColum.push({
                        x1: 50 - 48 / 3,
                        x2: 50 - 48 / 3,
                        y1: (i - 1) * midDot - this.elHeight / 36,
                        y2: i * midDot - this.elHeight / 36
                    })
                    groupRow.push({
                        x1: 50 - 48 / 3,
                        x2: i == 2 ? 50 - 48 * 3 / 3 : 50 - 48 * 2 / 3,
                        y1: ((i) * midDot - this.elHeight / 36 + (i - 1) * midDot - this.elHeight / 36) / 2,
                        y2: ((i) * midDot - this.elHeight / 36 + (i - 1) * midDot - this.elHeight / 36) / 2,
                    })
                }
            }
            groupColum.push({
                x1: 50 - 48 * 2 / 3,
                x2: 50 - 48 * 2 / 3,
                y1: ((4) * midDot - this.elHeight / 36 + (3) * midDot - this.elHeight / 36) / 2,
                y2: ((10) * midDot - this.elHeight / 36 + (9) * midDot - this.elHeight / 36) / 2
            })

            groupRow.push({
                x1: 50 - 48 * 2 / 3,
                x2: 50 - 48 * 3 / 3,
                y1: ((14) * midDot + (12) * midDot - 4 * this.elHeight / 36) / 4,
                y2: ((14) * midDot + (12) * midDot - 4 * this.elHeight / 36) / 4
            })

            groupRow.push({
                x1: 50 - 48 * 2 / 3,
                x2: 50 - 48 * 3 / 3,
                y1: ((30) * midDot + (28) * midDot - 4 * this.elHeight / 36) / 4,
                y2: ((30) * midDot + (28) * midDot - 4 * this.elHeight / 36) / 4
            })

            groupColum.push({
                x1: 50 - 48 * 2 / 3,
                x2: 50 - 48 * 2 / 3,
                y1: ((12) * midDot - this.elHeight / 36 + (11) * midDot - this.elHeight / 36) / 2,
                y2: ((18) * midDot - this.elHeight / 36 + (17) * midDot - this.elHeight / 36) / 2
            })

            groupColum.push({
                x1: 50 - 48 * 3 / 3,
                x2: 50 - 48 * 3 / 3,
                y1: ((2) * midDot - this.elHeight / 36 + (1) * midDot - this.elHeight / 36) / 2,
                y2: ((15) * midDot - this.elHeight / 36 + (14) * midDot - this.elHeight / 36) / 2
            })

            let group = groupRow.concat(groupColum);
            return group;
        },
        calcRMSEHeat(data, smooth_dataSet, raw_data, width, height) {
            let margin = ({ top: 20, right: 20, bottom: 30, left: 50 });
            // let sdata = [];
            let maxRmse = -999999;
            let minRmse = 999999;
            let maxTime = -999999;
            let maxError = -999999;
            let minError = 999999;
            let maxRaw = -999999;
            let minRaw = 999999;
            let maxCorr = -999999;
            let minCorr = 999999;
            let heatDataSet = [];
            let heatBeforeDataSet = [];
            let id_cnt = 0;
            for (let kk in smooth_dataSet) {
                let heat_data = [];
                let heatBefore_data = [];
                let smooth_data = smooth_dataSet[kk];
                let skipLength = this.skip_length[parseInt(kk)];
                // console.log(smooth_data, skipLength);
                for (let i = 0; i < 840; i += (i == 0 && 840 % skipLength != 0 ? 840 % skipLength : skipLength)) {
                    let skp = (i == 0 && 840 % skipLength != 0 ? 840 % skipLength : skipLength);
                    let rawTempValue = raw_data.slice(i, i + skp).map(d => parseFloat(d.value)).sort((a, b) => a - b)
                    let rawSum = sum(rawTempValue);
                    let smoothTempValue = smooth_data.slice(i, i + skp).map(d => parseFloat(d.value)).sort((a, b) => a - b)
                    let smoothSum = sum(smoothTempValue);
                    heatBefore_data.push({
                        rawData: smoothSum / smoothTempValue.length,
                        errorData: Math.abs(rawSum / rawTempValue.length - smoothSum / smoothTempValue.length),
                        time: i,
                        rmse: 0,
                        corr: 0,
                        skip: skp,
                        id: parseInt(kk),
                        fill_opacity: 0,
                        id_cnt: '_1'
                        // x: x(parseInt(raw_data[i].id)),
                        // w: Math.abs(x(parseInt(raw_data[i + ((i + skipLength < raw_data.length) ? skipLength : (raw_data.length - 1 - i))].id)) - x(parseInt(raw_data[i].id))),
                    });
                    maxError = Math.max(maxError, Math.abs(rawSum / rawTempValue.length - smoothSum / smoothTempValue.length));
                    minError = Math.min(minError, Math.abs(rawSum / rawTempValue.length - smoothSum / smoothTempValue.length));
                    maxRaw = Math.max(maxRaw, smoothSum / smoothTempValue.length);
                    minRaw = Math.min(minRaw, smoothSum / smoothTempValue.length);
                }
                heatBeforeDataSet.push(heatBefore_data);
                for (let i = 840; i < raw_data.length; i += skipLength) {
                    let rawTempValue = raw_data.slice(i, i + skipLength).map(d => parseFloat(d.value)).sort((a, b) => a - b)
                    let rawSum = sum(rawTempValue);
                    let smoothTempValue = smooth_data.slice(i, i + skipLength).map(d => parseFloat(d.value)).sort((a, b) => a - b)
                    let smoothSum = sum(smoothTempValue);
                    heat_data.push({
                        rawData: smoothSum / smoothTempValue.length,
                        errorData: Math.abs(rawSum / rawTempValue.length - smoothSum / smoothTempValue.length),
                        time: i,
                        rmse: 0,
                        corr: 0,
                        skip: skipLength,
                        id: parseInt(kk),
                        fill_opacity: 1,
                        id_cnt: id_cnt++
                            // x: x(parseInt(raw_data[i].id)),
                            // w: Math.abs(x(parseInt(raw_data[i + ((i + skipLength < raw_data.length) ? skipLength : (raw_data.length - 1 - i))].id)) - x(parseInt(raw_data[i].id))),
                    });
                    maxError = Math.max(maxError, Math.abs(rawSum / rawTempValue.length - smoothSum / smoothTempValue.length));
                    minError = Math.min(minError, Math.abs(rawSum / rawTempValue.length - smoothSum / smoothTempValue.length));
                    maxRaw = Math.max(maxRaw, smoothSum / smoothTempValue.length);
                    minRaw = Math.min(minRaw, smoothSum / smoothTempValue.length);
                }
                heatDataSet.push(heat_data);
            }
            // console.log(heatBeforeDataSet);

            let lineData = [];
            for (let i in data) {
                let startPos = 840;
                let tp = [];
                for (let j in data[i]) {
                    // sdata.push({
                    //     id: i,
                    //     skip: this.skip_length[i],
                    //     time: j * this.skip_length[i] + startPos,
                    //     rmse: parseFloat(data[i][j]['rmse'])
                    // });
                    tp.push({
                        id: i,
                        skip: this.skip_length[i],
                        time: j * this.skip_length[i] + startPos,
                        errorData: 0,
                        rmse: parseFloat(data[i][j]['rmse']),
                        corr: parseFloat(data[i][j]['129_pearson'])
                    });
                    // console.log(data[i][j]['129_pearson'])
                    maxTime = Math.max(maxTime, j * this.skip_length[i] + startPos);
                    maxRmse = Math.max(maxRmse, parseFloat(data[i][j]['rmse']));
                    minRmse = Math.min(minRmse, parseFloat(data[i][j]['rmse']));
                    maxCorr = Math.max(maxCorr, parseFloat(data[i][j]['129_pearson']));
                    if (parseFloat(data[i][j]['129_pearson']) != 0)
                        minCorr = Math.min(minCorr, parseFloat(data[i][j]['129_pearson']));
                }
                lineData.push(tp);
            }
            // console.log(heatDataSet)
            // console.log(lineData);
            // console.log(maxCorr, minCorr);


            for (let i in heatDataSet) {
                for (let j in heatDataSet[i]) {
                    heatDataSet[i][j]['rmse'] = lineData[parseInt(i)][j]['rmse'];
                    heatDataSet[i][j]['corr'] = lineData[parseInt(i)][j]['corr'];
                    heatBeforeDataSet[i].push(heatDataSet[i][j])
                }
                heatBeforeDataSet[i] = heatBeforeDataSet[i].concat(heatDataSet[i]);
            }
            let HeatSumData = [];
            // for (let i = 0; i < 4; ++i) {
            //     HeatSumData.push(lineData[i]);
            // }
            for (let i = 0; i < heatBeforeDataSet.length; ++i) {
                HeatSumData.push(heatBeforeDataSet[i]);
            }

            // for (let i = 0; i < heatDataSet.length; ++i) {
            //     HeatSumData.push(heatDataSet[i]);
            // }
            let rawScale = scaleLinear([minRaw, maxRaw], [0, 1]);
            let rmseScale = scaleLinear([minRmse, maxRmse], [0, 1]);
            let errorScale = scaleLinear([minError, maxError], [0, 1]);
            let corrScale = scaleLinear([minCorr, maxCorr], [0, 1]);
            let timeScale = scaleLinear([0, maxTime], [margin.left, width - margin.right]);
            let quantization1 = vsup.quantization().branching(2).layers(4).valueDomain([minError, maxError]).uncertaintyDomain([(maxRaw), minRaw]);
            let quantization2 = vsup.quantization().branching(2).layers(4).valueDomain([minRmse, maxRmse]).uncertaintyDomain([(maxCorr), minCorr]);

            let heatColor = interpolateYlOrRd;
            let heatScale1 = vsup.scale().quantize(quantization1).range(heatColor);
            let heatScale2 = vsup.scale().quantize(quantization2).range(heatColor);

            // var legend = vsup.legend.arcmapLegend();

            // legend
            //     .scale(heatScale)
            //     .size(160)
            //     .x(200)
            //     .y(100)
            //     .vtitle("Difference")
            //     .utitle("RMSE");
            // select('#legend_g').append('g')
            // .call(legend)
            // let xAxis = axisBottom(timeScale).ticks(10);
            // let yAxis = axisLeft(rmseScale).ticks(10);
            // select("#x_axis_g").call(xAxis);
            // select("#y_axis_g").call(yAxis);
            let res_data = [];
            for (let i in HeatSumData) {
                for (let j in HeatSumData[i]) {
                    // console.log(lineData[i][j].skip)
                    HeatSumData[i][j].x = timeScale(HeatSumData[i][j].time);
                    HeatSumData[i][j].w = timeScale(HeatSumData[i][j].skip);
                    HeatSumData[i][j].v = rmseScale(HeatSumData[i][j].rmse);
                    HeatSumData[i][j].id_cnt = HeatSumData[i][j].id_cnt;
                    HeatSumData[i][j].h = height / 36 - 3
                    HeatSumData[i][j].y = parseInt(HeatSumData[i][j].id) * height / 36;
                    HeatSumData[i][j].rmseColor = heatColor(HeatSumData[i][j].v);
                    HeatSumData[i][j].errorColor = heatColor(errorScale(HeatSumData[i][j].errorData));
                    HeatSumData[i][j].rawColor = heatColor(rawScale(HeatSumData[i][j].rawData));
                    HeatSumData[i][j].corrColor = heatColor(corrScale(HeatSumData[i][j].corr));
                    HeatSumData[i][j].vsupColor1 = heatScale1((HeatSumData[i][j].errorData), (HeatSumData[i][j].rawData));
                    HeatSumData[i][j].vsupColor2 = heatScale2((HeatSumData[i][j].rmse), HeatSumData[i][j].corr);
                    HeatSumData[i][j].colorMap = [HeatSumData[i][j].vsupColor1, HeatSumData[i][j].rawColor, HeatSumData[i][j].errorColor, HeatSumData[i][j].vsupColor2, HeatSumData[i][j].rmseColor, HeatSumData[i][j].corrColor];
                }
                res_data.push({
                    h: height / 36,
                    heat: HeatSumData[i]
                })
            }
            // console.log(res_data);

            return res_data;
        },
        calcResultData(data, heatData) {
            let res_data = new Object();
            let max_train = 0,
                max_test = 0,
                max_acf = 0
            for (let i in data) {
                if (i == '9' || i == '10')
                    continue;
                for (let j in data[i].predic_info) {
                    res_data[data[i].dataset_name + '_skip' + data[i].predic_info[j].skip] = data[i].predic_info[j];
                    // console.log(data[i].predic_info[j]['ACF'], i, j)
                    max_acf = Math.max(max_acf, data[i].predic_info[j]['ACF']);
                    max_train = Math.max(max_train, data[i].predic_info[j]['loss=mean_squared_error']);
                    max_test = Math.max(max_test, data[i].predic_info[j]['val_loss=val_mse']);
                }
            }
            // console.log(max_acf);
            let leftT = 140;
            let barS = heatData[0].heat[0].x - leftT;
            let trainScale = scaleLinear([0, max_train], [0, ((barS) / 3) * 0.9]);
            let testScale = scaleLinear([0, max_test], [0, ((barS) / 3) * 0.9]);
            let acfScale = scaleLinear([0, max_acf], [0, ((barS) / 3) * 0.9]);

            for (let i in heatData) {
                heatData[i]['res'] = [{
                    x: leftT,
                    w: trainScale(res_data[this.filename[i].substring(0, this.filename[i].length - 8)]['loss=mean_squared_error']),
                    y: i * this.elHeight / 36,
                    h: this.elHeight / 36 - 3
                }, {
                    x: leftT + (barS) / 3,
                    w: testScale(res_data[this.filename[i].substring(0, this.filename[i].length - 8)]['val_loss=val_mse']),
                    y: i * this.elHeight / 36,
                    h: this.elHeight / 36 - 3
                }, {
                    x: leftT + 2 * (barS) / 3,
                    w: acfScale(res_data[this.filename[i].substring(0, this.filename[i].length - 8)]['ACF']),
                    y: i * this.elHeight / 36,
                    h: this.elHeight / 36 - 3
                }]
            }
            return heatData;
        }
    },
    created() {},
    mounted() {
        // this.elHeight = this.$refs.DataTransformation.offsetHeight;
        // this.elWidth = this.$refs.DataTransformation.offsetWidth;
        this.tlHeight = this.$refs.timeline.offsetHeight * 1;
        this.heatHeight = this.$refs.timeline.offsetHeight * 0.3;
        this.tlWidth = this.$refs.timeline.offsetWidth;

        // this.calcTimeLine(SN_raw_data, this.tlHeight, this.tlWidth);

        const dataStore = useDataStore();
        let _this = this;

        dataStore.$subscribe((mutation, state) => {
            if (dataStore.select_row != null) {
                let sel_row = dataStore.select_row;
                console.log(sel_row);
                select('#brush_g').call(this.timeBrush.move, [this.allTimeScale(sel_row.time), this.allTimeScale(sel_row.time + 120)]);

                let lineGenerate = line()
                    .x(d => _this.xScale(d.id))
                    .y(d => _this.yScale(d.value));
                this.predict_tag = 1;
                this.predict_line = sel_row.predict_line;
                selectAll('#sel_predict_line').remove();
                select('#brush_path_g').append('path').attr('d', lineGenerate(sel_row.predict_line)).attr('id', 'sel_predict_line').attr('stroke', 'red').attr('stroke-width', 2).attr('fill', 'none');
            }
        })

    },
}
</script>

<style>
/* *,
*::before,
*::after {
    font-weight: normal;
} */

#DataTransformation {
    font-size: 20px;
    /* font-family: Roboto; */
}

.el-table .el-table__cell {
    padding: 0px;
}

.selection {
    fill-opacity: 0.15;
}
</style>
