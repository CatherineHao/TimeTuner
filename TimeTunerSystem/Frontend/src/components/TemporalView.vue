<!--
 *                        _oo0oo_
 *                       o8888888o
 *                       88" . "88
 *                       (| -_- |)
 *                       0\  =  /0
 *                     ___/`---'\___
 *                   .' \\|     |// '.
 *                  / \\|||  :  |||// \
 *                 / _||||| -:- |||||- \
 *                |   | \\\  - /// |   |
 *                | \_|  ''\---/''  |_/ |
 *                \  .-\__  '-'  ___/-. /
 *              ___'. .'  /--.--\  `. .'___
 *           ."" '<  `.___\_<|>_/___.' >' "".
 *          | | :  `- \`.;`\ _ /`;.`/ - ` : | |
 *          \  \ `_.   \_ __\ /__ _/   .-` /  /
 *      =====`-.____`.___ \_____/___.-`___.-'=====
 *                        `=---='
 * 
 * 
 *      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 * 
 *            佛祖保佑     永不宕机     永无BUG
 -->

<!--
 * @Description: 
 * @Author: Qing Shi
 * @Date: 2023-01-10 21:20:01
 * @LastEditTime: 2023-03-27 04:48:50
-->
<template>
    <div class="frameworkTitle" style="padding-right: 10px;">
        <div class="title">Temporal View</div>
        <p class="titleTriangle"></p>

        <div style="float: right; margin-top: 3px; height: 30px;">
            <span>
                <svg width="655" height="30" style="margin-right: 40px; margin-top: 3px;">
                    <g transform="translate(100, 0)">
                        <g transform="translate(300, 0)">
                            <text x="0" y="20" font-size="15" text-anchor="end">{{ nameLine[0] }} </text>
                            <path d="M10,15L70,15" stroke-width="5" :fill="'none'" :stroke="'#c0c0c0'"></path>
                        </g>
                        <g v-if="showLineLegend">
                            <g transform="translate(0, 0)">
                                <text x="10" y="20" font-size="15" text-anchor="end">{{ nameLine[1] }} </text>
                                <path d="M20,15L80,15" stroke-width="5" :fill="'none'" :stroke="colorLine[0]"></path>
                            </g>
                            <g transform="translate(150, 0)">
                                <text x="10" y="20" font-size="15" text-anchor="end">{{ nameLine[2] }} </text>
                                <path d="M20,15L80,15" stroke-width="5" :fill="'none'" :stroke="colorLine[1]"></path>
                            </g>
                        </g>
                    </g>
                    <g transform="translate(500, 0)">
                        <text x="10" y="20" font-size="15">Layer: </text>
                        <rect v-for="(o, i) in horizon_color" :key="'hor_' + i" :x="i * 25 + 55" :y="5" :width="20"
                            height="20" :fill="o" stroke="black"></rect>
                    </g>
                </svg>
            </span>
            <span style="margin-right: 0px; position: absolute; right: 0px;">
                <el-button style="height: 30px;" @click="refresh()">

                    <svg t="1680060651492" class="icon" viewBox="0 0 1024 1024" version="1.1"
                        xmlns="http://www.w3.org/2000/svg" p-id="2903" width="20" height="20">
                        <path
                            d="M810.666667 273.706667L750.293333 213.333333 512 451.626667 273.706667 213.333333 213.333333 273.706667 451.626667 512 213.333333 750.293333 273.706667 810.666667 512 572.373333 750.293333 810.666667 810.666667 750.293333 572.373333 512z"
                            p-id="2904" fill="#606266"></path>
                    </svg>
                </el-button>
            </span>
        </div>
    </div>
    <div class="frameworkBody">

        <div style="height: calc(100%); width: 100%; margin-top: 0px;">
            <div style="height: 96%; width: 100%;" ref="timeline">
                <svg width="100%" height="100%">
                    <g v-for="(item, i) in overview_line_data" :transform="translate(0, item.posHeight, 0)">
                        <clipPath id="clipPathHorizon">
                            <rect :x="0" :y="0" :width="tlWidth" :height="30"></rect>
                        </clipPath>

                        <g v-if="item.rowHeight == 35 ? 0 : 1">

                            <clipPath id="clipPathLine">
                                <rect :x="50" :y="0" :width="tlWidth - 50 - 10" :height="item.rowHeight - 30"></rect>
                            </clipPath>
                            <g :id="'time_line_legend' + i" :transform="translate(0, 0, 0)"></g>

                            <g :id="'time_line' + i" :transform="translate(0, 0, 0)" clip-path="url(#clipPathLine)">
                                <path :id="'time_path_raw' + i" :d="timeLinePath" :fill="'none'" :stroke="'#c0c0c0'"
                                    stroke-width="3"></path>
                                <g v-if="showLineLegend">
                                    <path v-for="(pl, pi) in overLinePath" :key="'pl' + pi" :d="pl" :fill="'none'"
                                        :stroke="colorLine[pi]" stroke-width="3" :id="'plid' + pi"></path>
                                </g>
                            </g>
                        </g>
                        <g clip-path="url(#clipPathHorizon)" :id="'brush_area' + i"
                            :transform="translate(0, item.rowHeight - 30, 0)">
                            <path :d="item.d" :stroke="'none'" :fill="item.fill[0]"
                                :transform="translate(0, -item.height * 3, 0)"></path>
                            <path :d="item.d" :stroke="'none'" :fill="item.fill[1]"
                                :transform="translate(0, -item.height * 2, 0)"></path>
                            <path :d="item.d" :stroke="'none'" :fill="item.fill[2]"
                                :transform="translate(0, -item.height * 1, 0)"></path>
                            <path :d="item.d" :stroke="'none'" :fill="item.fill[3]"></path>
                        </g>
                        <g :transform="translate(0, item.rowHeight - 30, 0)" style="cursor: pointer;"
                            @click="clickAttribute(i)">
                            <text x="0" y="18" font-size="14"
                                :text-decoration="selectSmoothObj[item.feature] == 1 ? 'underline' : ''"
                                text-anchor="start">{{ item.feature }}</text>
                        </g>
                    </g>
                </svg>
                <!-- </div> -->
            </div>

            <div style="height: 4%;">
                <svg width="100%" height="100%">
                    <g id="global_time_axis"></g>
                </svg>
            </div>
        </div>

    </div>
</template>

<script>
import { axisBottom, axisLeft } from 'd3-axis';
import { scaleLinear, scaleOrdinal, scaleUtc } from 'd3-scale';
import { arc, area, line } from 'd3-shape';
// import SN_raw_data from "../assets/SN_m_tot_V2.0.csv";
import uni_var_data from "../assets/allData/univariate_data/all_smooth_value.csv";
import multi_var_data from "../assets/allData/multivariate_data/all_smooth_multi15.csv";
// import multi_var_data from "../assets/allData/multivariate_data/smooth_data/raw_15month.csv";
import { extent, max, min, sum } from 'd3-array';
import { brushX } from 'd3-brush';
import { select, selectAll, selectorAll } from 'd3-selection';
import { scale } from 'vsup';
// import { ConstantTypes } from '@vue/compiler-core';
import { useDataStore } from "../stores/counter";
// import { isNumber } from 'element-plus/es/utils';
export default {
    name: 'DataTransformationView',
    props: [],
    data () {
        return {
            showLineLegend: 0,
            colorLine: ['#A50021', '#181CF7'],
            overLinePath: [],
            nameLine: ['', '', ''],
            overLine: [],
            horizon_level: 4,
            elHeight: 1000,
            elWidth: 1000,
            tlHeight: 1000,
            tlWidth: 300,
            featureSet: [],
            showTag: '',
            heatHeight: 0,
            heatTag: 3,
            timeBrush: null,
            timeBrush_g: null,
            allTimeScale: null,
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
            smoothTag: 0,
            timeLinePath: null,
            linePathTag: 0,
            coverRect: [],
            predict_line: [],
            predict_tag: 0,
            overview_line_data: [],
            horizon_color: ['#c7dbee', '#a1cadf', '#4892c3', '#0e4591'],
            dataSet: [],
            sdData: '',
            timeScaleGlobal: null,
            brushMoveData: {
                'sunspots': ['1900-01-01', '1930-01-01'],
                'pm': ['2013-11-24', '2014-2-16']
            },
            brushDyMoveData: [],
            brushTempMove: [],
            datasetSelect: 'sunspots',
            smoothSelect: {},
            selectAttribute: 0,
            selectSmooth: [],
            selectSmoothObj: {},
            timeMap: [],
            openFeature: 'pm25',
            smoothFeature: 'raw',
            allData: [],
            allFeatureSet: []
        }
    },
    methods: {
        refresh () {
            this.showLineLegend = 0;
            this.overLinePath = [];
            this.selectSmoothObj = {};
            const dataStore = useDataStore();
            dataStore.selectSmooth = [];
            this.brushTempMove = this.brushMoveData[this.datasetSelect];
            this.showDetail(this.selectAttribute, '#time_line_legend' + this.selectAttribute)
        },
        clickAttribute (num) {
            // console.log(num)
            this.selectAttribute = num;
            this.showDetail(this.selectAttribute, '#time_line_legend' + num)
        },
        timeFormat: function (time, type) {
            // console.log(time);
            if (!isNaN(Number(time,10)))
                time = time.toString();
            let timeFormatRes = '';
            if (type == 'sunspots') {
                let year = time.slice(0, 4);
                let month = time.slice(-2);
                let day = '01';
                timeFormatRes = year + '-' + month + '-' + day;
            } else {
                let [date, detail] = time.split(' ');
                // console.log(date, detail);
                let year = date.slice(0, 4);
                let month = date.slice(4, 6);
                let day = date.slice(-2);
                timeFormatRes = year + '-' + month + '-' + day + ' ' + detail;
            }
            return new Date(timeFormatRes);
        },
        calcTimeScale: function (data, type) {
            // console.log(data);
            let margin = ({ top: 30, right: 15, bottom: 50, left: 50 });
            let raw_time_data = [];
            let timeData = [];
            for (let i in data) {

                timeData.push(this.timeFormat(data[i]['time'], type));
                raw_time_data.push(data[i]['time']);
                // if (type == 'sunspots') {
                //     timeData.push(this.timeFormat(data[i]['timestamp'], type));
                //     raw_time_data.push(data[i]['timestamp']);
                // } else {
                //     timeData.push(this.timeFormat(data[i]['date'], type));
                //     raw_time_data.push(data[i]['date']);
                // }
            }
            let timeScale = scaleUtc(extent(timeData), [margin.left, this.tlWidth - margin.right]);
            this.timeScaleGlobal = timeScale;
            selectAll('#global_time_axis_g').remove();
            select('#global_time_axis').append('g').attr('id', 'global_time_axis_g')
                .call(axisBottom(timeScale).ticks((this.elWidth - margin.left - margin.right) / 80).tickSizeOuter(0))
            // if 
            return raw_time_data;
        },
        showDetail (cnt, id) {
            // console.log(id);
            this.brushDyMoveData = this.brushTempMove;
            // console.log(this.featureSet, this.dataSet)
            if (this.datasetSelect == 'sunspots')
                this.nameLine[0] = this.featureSet[cnt] + ':';
            else
                this.nameLine[0] = 'Raw:';
            let sigHeight = 0;
            for (let i in this.overview_line_data) {
                this.overview_line_data[i].posHeight = sigHeight;
                if (i == cnt)
                    this.overview_line_data[i].rowHeight = this.tlHeight - (this.featureSet.length - 1) * 35 - 3;
                else
                    this.overview_line_data[i].rowHeight = 35;
                sigHeight += this.overview_line_data[i].rowHeight;
            }
            // console.log(this.dataSet, this.featureSet[cnt], cnt);
            this.calcTimeLine(this.dataSet[this.featureSet[cnt]], this.tlHeight - this.featureSet.length * 30 - 50, this.tlWidth, id);
            this.setupBrush(this.dataSet[this.featureSet[cnt]], '#brush_area' + cnt, this.tlWidth, this.tlHeight - this.featureSet.length * 30 - 20, cnt);
        },
        translate (x, y, deg) {
            return `translate(${x}, ${y}) rotate(${deg})`;
        },
        setupBrush: function (data, id, width, height, cnt) {
            // console.log('brush')
            let focusHeight = 30;
            let margin = ({ top: -20, right: 15, bottom: 50, left: 50 });
            const timeBrush = brushX()
                .extent([
                    [margin.left, 0],
                    [width - margin.right, 30]
                ])
                .on('start', brushStart)
                .on('brush', brushed)
                .on('end', brushEnd);
            // console.log('brush_0')
            // if (this.timeBrush != null) {
            //     this.timeBrush.remove()
            // }
            this.timeBrush = timeBrush;
            // let x = scaleLinear()
            //     .domain([0, data.length - 1])
            //     .range([margin.left, width - margin.right])
            let x = scaleUtc(extent(data, d => this.timeFormat(d.date, this.datasetSelect)), [margin.left, width - margin.right]);
            this.allTimeScale = x;

            let _this = this;
            let radius = focusHeight / 2 - 10;

            let brushHandle = (g, s) => g
                .selectAll(".handle--custom")
                .data([{ type: "w" }, { type: "e" }])
                .join(
                    enter => enter.append("path")
                        .attr("class", "handle--custom")
                        .attr("fill", "white")
                        .attr("opacity", 1)
                        .attr("stroke", "#777")
                        .attr("stroke-width", 3)
                        .attr("cursor", "ew-resize")
                        .attr("d", 'M -5 ' + (focusHeight / 2 + 30) + ' L -5 ' + (focusHeight / 2 + 0) + 'L 5 ' + (focusHeight / 2 + 0) + ' L 5 ' + (focusHeight / 2 + 30) + ' Z'),
                )
                .attr("display", s === null ? "none" : null)
                .attr("transform", s === null ? null : (d, i) => `translate(${s[i]},${radius + margin.top})`)

            function brushStart () {
                // console.log(222)
                selectAll('.sparkbox').remove();
            }

            function brushEnd ({ selection }) {
                let timeStep = [_this.timeScaleGlobal.invert(selection[0]), _this.timeScaleGlobal.invert(selection[1])];
                // console.log(timeStep)
                _this.brushTempMove = timeStep;

                _this.xScale.domain(timeStep);
                // console.log(_this.xScale.domain(), _this.xScale.range());
                // _this.yScale.domain([0, maxY]);
                // let xAxis = [];
                // let timeRange = [];
                // let lenRange = [];
                // let cnt_i = 0
                // for (let ii = timeStep[0]; ii <= timeStep[1]; ii += Math.floor(timeStep[1] - timeStep[0]) / 10) {
                //     // console.log(i, _this.lineData);
                //     let i = parseInt(ii);
                //     cnt_i = i;
                //     xAxis.push({
                //         x: _this.xScale(i),
                //         y: 0,
                //         // text: parseInt(parseInt(_this.lineData[i].timestamp) / 100) + '.' + parseInt(parseInt(_this.lineData[i].timestamp) % 100)
                //         text: (_this.lineData[i].timestamp)
                //     });
                //     timeRange.push(_this.lineData[i].timestamp);
                //     lenRange.push(_this.xScale(i))
                // }
                // if (timeRange.length == 10) {
                //     timeRange.push('');
                //     lenRange.push(_this.elWidth - 20)
                // }
                // let tScale = scaleOrdinal(timeRange, lenRange)
                // // console.log(timeRange, lenRange);

                let marginX = ({ top: 30, right: 15, bottom: 40, left: 50 });
                selectAll('#axsg').remove();
                select('#time_line_legend' + cnt).append('g').attr('id', 'axsg').attr("transform", `translate(0, ${height - marginX.bottom})`).call(axisBottom(_this.xScale).ticks((_this.elWidth - marginX.left - marginX.right) / 80).tickSizeOuter(0));

                // _this.timeAxis = xAxis;

                let lineGenerate = line()
                    .x((d) => _this.xScale(_this.timeFormat(d.date, _this.datasetSelect)))
                    .y(d => _this.yScale(d.value));
                _this.lineGenerateFunc = lineGenerate;

                // _this.select_time_step = timeStep;

                select('#time_path_raw' + cnt).attr('d', lineGenerate(_this.lineData));
                // if (_this.smoothTag) {

                //     select('#time_path_selected').attr('d', lineGenerate(_this.smoothLineData));
                // }
                if (_this.showLineLegend) {
                    for (let i in _this.overLine) {

                        select('#plid' + i).attr('d', lineGenerate(_this.overLine[i]));
                    }
                }
            }

            function brushed ({ selection }) {
                // console.log(selection);
                // let timeStep = [parseInt(_this.rxScale(selection[0])), parseInt(_this.rxScale(selection[1]))];

                let timeStep = [_this.timeScaleGlobal.invert(selection[0]), _this.timeScaleGlobal.invert(selection[1])];
                // console.log(timeStep)
                _this.xScale.domain(timeStep);
                // _this.yScale.domain([0, maxY]);
                let xAxis = [];
                let timeRange = [];
                let lenRange = [];
                let cnt_i = 0
                // select("#timeline_g").append('path').attr('id', 'selected_area').attr('d', 'M ' + parseInt(988) + ' ' + 85 + ' L ' + parseInt(1760) + ' ' + 85 + ' L ' + (_this.elWidth) + ' 130 L 50 130 Z').attr('stroke', '#777').attr('stroke-width', 1).attr('fill', '#777').attr('opacity', 0.15);    
                // for (let ii = timeStep[0]; ii <= timeStep[1]; ii += Math.floor(timeStep[1] - timeStep[0]) / 10) {
                //     // console.log(i, _this.lineData);
                //     let i = parseInt(ii);
                //     cnt_i = i;
                //     xAxis.push({
                //         x: _this.xScale(i),
                //         y: 0,
                //         // text: parseInt(parseInt(_this.lineData[i].timestamp) / 100) + '.' + parseInt(parseInt(_this.lineData[i].timestamp) % 100)
                //         text: (_this.lineData[i].timestamp)
                //     });
                //     timeRange.push(_this.lineData[i].timestamp);
                //     lenRange.push(_this.xScale(i))
                // }
                // if (timeRange.length == 10) {
                //     timeRange.push('');
                //     lenRange.push(_this.elWidth - 20)
                // }
                // let tScale = scaleOrdinal(timeRange, lenRange)
                // // console.log(timeRange, lenRange);
                let marginX = ({ top: 30, right: 15, bottom: 40, left: 50 });
                selectAll('#axsg').remove();
                select('#time_line_legend' + cnt).append('g').attr('id', 'axsg').attr("transform", `translate(0, ${height - marginX.bottom})`).call(axisBottom(_this.xScale).ticks((_this.elWidth - marginX.left - marginX.right) / 80).tickSizeOuter(0));
                // console.log('#time_line_legend' + cnt);

                // // _this.timeAxis = xAxis;

                let lineGenerate = line()
                    .x((d) => _this.xScale(_this.timeFormat(d.date, _this.datasetSelect)))
                    .y(d => _this.yScale(d.value));

                // _this.select_time_step = timeStep;

                select('#time_path_raw' + cnt).attr('d', lineGenerate(_this.lineData));
                // console.log(_this.showLineLegend)
                if (_this.showLineLegend) {
                    // console.log(1111, _this.overLine)
                    for (let i in _this.overLine) {
                        // console.log(lineGenerate(_this.overLine[i]));
                        select('#plid' + i).attr('d', lineGenerate(_this.overLine[i]));
                    }
                }
                // if (_this.predict_tag) {

                //     select('#sel_predict_line').attr('d', lineGenerate(_this.predict_line));
                // }

                select("#selected_area").attr('d', 'M ' + parseInt(selection[0]) + ' ' + 441 + ' L ' + parseInt(selection[1]) + ' ' + 441 + ' L ' + (_this.tlWidth - margin.right) + ' 393 L 50 393 Z')
                select(this).call(brushHandle, selection);

                // console.log(timeStep);
                // _this.calcTimeLineCompare(data, [], _this.tlHeight, _this.tlWidth, _this.select_time_step)
                // let d = _this.calcTimeLineCompare(SN_raw_data, [], _this.tlHeight, _this.tlWidth, _this.select_time_step); 

                // _this.rawTimeLineData = d[0];
                // _this.smoothTimeLineData = d[1];
            }
            // console.log(select(id))
            if (this.timeBrush_g != null) {
                this.timeBrush_g.remove();
            }
            this.timeBrush_g = select(id).append('g').call(timeBrush)
                .call(timeBrush.move, [x(new Date(_this.brushDyMoveData[0])), x(new Date(_this.brushDyMoveData[1]))]);

        },
        calcTimeLine (data, height, width, id) {
            // console.log(data)
            // data = data.slice(0, 1000)
            let margin = ({ top: 25, right: 15, bottom: 10, left: 50 });
            let focusHeight = 100;

            let y = scaleLinear()
                .domain([min(data, d => parseFloat(d.value)), max(data, d => parseFloat(d.value))])
                .range([height - margin.bottom, margin.top])
            // console.log(data);
            // console.log();
            // console.log(y.domain())
            // for (let i in data) {
            //     console.log(data[i])
            // }
            // let x = scaleLinear()
            //     .domain([0, max(data, d => parseInt(d.id))])
            //     .range([margin.left, width - margin.right])
            let x = scaleUtc().domain(extent(data, d => this.timeFormat(d.date, this.datasetSelect))).range([margin.left, width - margin.right]);
            // console.log(extent(data, d => this.timeFormat(d.date, this.datasetSelect)))
            // let x = scaleLinear([0, data.length - 1], [margin.left, width - margin.right]);
            // const rx = scaleLinear()
            //     .domain([margin.left, width - margin.right])
            //     .range([0, max(data, d => parseInt(d.id))]);
            const rx = scaleLinear()
                .domain([margin.left, width - margin.right])
                .range(extent(data, d => this.timeFormat(d.date, this.datasetSelect)));

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
                .x((d, i) => {
                    // console.log(d, d.date, (this.timeFormat(d.date, this.datasetSelect)), x(this.timeFormat(d.date, this.datasetSelect)))
                    return x(this.timeFormat(d.date, this.datasetSelect))
                })
                .y(d => y(parseFloat(d.value)));
            this.lineGenerateFunc = lineGenerate;

            let yAxis = (g, y, title) => g
                .attr("transform", `translate(${margin.left},${0})`)
                .call(axisLeft(y))
                // .call(g => g.select(".domain").remove())
                .call(g => g.selectAll(".title").data([title]).join("text")
                    .attr("class", "title")
                    .attr("x", -30)
                    .attr("y", 15)
                    .attr("fill", "currentColor")
                    .attr("text-anchor", "middle")
                    .attr('font-size', '14px')
                    .attr('font-family', 'Arial')
                    .text(title));
            selectAll('#yAxis_g').remove();
            // console.log(id)
            select(id).append('g').attr('id', 'yAxis_g').call(yAxis, y, 'Value');
            this.timeLinePath = lineGenerate(data);
            // console.log(data)
            this.lineData = data;
            // console.log(this.timeLinePath)
        },
        calcMonth (startTime, endTime) {
            let year = parseInt(endTime / 100) - parseInt(startTime / 100);
            let month = endTime % 100 - startTime % 100 + 1;
            let sumMonth = year * 12 + month;
            return sumMonth;
        },
        calcFeatureLine (data, width, height) {
            let margin = { left: 0, right: 0, top: 0, bottom: 0 };
            let xScale = scaleLinear([0, data.length - 1], [margin.left, width - margin.right]);
            let vRange = extent(data, d => parseFloat(d.value));
            let yScale = scaleLinear(vRange, [height - margin.bottom, margin.top]);
            let lineGenerate = line().x((d, i) => xScale(i)).y(d => yScale(parseFloat(d.value)));
            let line_data = lineGenerate(data);
            return line_data;
        },
        calcFeatureArea (data, width, height) {
            let margin = { left: 50, right: 15, top: 0, bottom: 0 };

            let xScale = scaleLinear([0, data.length - 1], [margin.left, width - margin.right]);
            let vRange = extent(data, d => parseFloat(d.value));
            // console.log(vRange);
            // vRange
            let yScale = scaleLinear(vRange, [this.horizon_level * (height - margin.bottom), margin.top]);
            let areaGenerate = area().x((d, i) => xScale(parseFloat(i))).y0(d => yScale(parseFloat(d.value))).y1(d => yScale(parseFloat(vRange[0])));
            let area_data = areaGenerate(data);
            return area_data;
        },
        calcOverviewTimeLine (data, filter_name) {
            // console.log(data);
            let featureSet = [];
            let all_feature = [];
            let all_data = {};
            let allData = {};
            // console.log(filter_name);
            for (let i in data[0]) {
                if (typeof (filter_name) == "object" && filter_name[i] != 1) {
                    continue;
                }
                if (i == 'time' || i == 'id')
                    continue;
                all_feature.push(i);
                all_data[i] = [];
                // if (this.datasetSelect == 'pm' && x[0] != 'raw')
                //     continue
                // if (i != 'value' && this.datasetSelect == 'sunspots')
                //     continue
                featureSet.push(i);
                allData[i] = [];
            }
            // console.log(featureSet);
            // featureSet = ['raw']
            // allData['raw'] = []
            for (let i in data) {
                for (const j of featureSet) {
                    // console.log(data[i][j])
                    let v = parseFloat(data[i][j]);
                    if (j == 'wnd_dir')
                        v = (v / 45).toFixed(0);
                    let date = data[i]['time'];
                    // if (this.datasetSelect == 'sunspots')
                    //     date = data[i]['timestamp']
                    // else
                    //     date = data[i]['date']
                    allData[j].push({
                        date: date,
                        value: v,
                        id: parseInt(i)
                    });
                }
            }
            // for (let i in data) {
            //     for (const j of all_feature) {
            //         // console.log(data[i][j])
            //         let v = parseFloat(data[i][j]);
            //         if (j == 'wnd_dir')
            //             v = (v / 45).toFixed(0);
            //         let date;
            //         if (this.datasetSelect == 'sunspots')
            //             date = data[i]['timestamp']
            //         else
            //             date = data[i]['date']
            //         all_data[j].push({
            //             date: date,
            //             value: v,
            //             id: parseInt(i)
            //         });
            //     }
            // }
            // console.log(allData);
            let result_data = new Array();
            // for (let i in allData) {
            //     result_data.push({
            //         d: this.calcFeatureLine(allData[i], this.tlWidth, this.tlHeight / (featureSet.length *2)),
            //         raw: allData[i],
            //         feature: i
            //     })
            // }
            let cnt_h = 0

            for (let i in allData) {
                let feature = i;
                result_data.push({
                    d: this.calcFeatureArea(allData[i], this.tlWidth, 30),
                    raw: allData[i],
                    feature: feature,
                    // feature: i,
                    featureName: i,
                    fill: this.horizon_color,
                    height: 30,
                    rowHeight: 30,
                    posHeight: cnt_h * 30
                })
                cnt_h++;
                // if (cnt_h == 6) 
                // break
            }
            // console.log(result_data);
            // console.log(allData);
            // console.log(featureSet)

            return [result_data, featureSet, allData, featureSet, allData];
        },
        dataConvert (data) {
            let featureSet = [];
            for (let i in data) {
                featureSet.push(i);
            }
            // console.log(data[featureSet[0]]);
            let res_data = [];
            for (let i in data[featureSet[0]]) {
                let tp = {};
                for (let j in featureSet) {
                    tp[featureSet[j]] = data[featureSet[j]][i];
                }
                // console.log(tp);
                res_data.push(tp);
            }
            return res_data;
        }
    },
    created () { },
    mounted () {
        this.tlHeight = this.$refs.timeline.offsetHeight * 1;
        this.tlWidth = this.$refs.timeline.offsetWidth;
        // this.tlHeight = 100;
        // console.log(SN_raw_data)
        // // this.dataSet = multi_var_data; 
        // this.sdData = 1


        // [this.overview_line_data, this.featureSet, this.dataSet, this.allFeatureSet, this.allData] = this.calcOverviewTimeLine(uni_var_data);
        // // console.log(this.overview_line_data, this.featureSet, this.dataSet);
        // this.brushTempMove = this.brushMoveData[this.datasetSelect];
        // this.timeMap = this.calcTimeScale(uni_var_data, this.datasetSelect);

        // console.log(this.dataSet);

        // this.setupBrush(uni_var_data, '#brush_area0', this.tlWidth, 0)


        // this.datasetSelect = 'sunspots';
        //             [this.overview_line_data, this.featureSet, this.dataSet, this.allFeatureSet, this.allData] = this.calcOverviewTimeLine(uni_var_data, {
        //                 "RAW": 1,
        //                 "MA-6": 1,
        //                 "WMA-6": 1
        //             });
        //             // console.log(this.overview_line_data, this.featureSet, this.dataSet);
        //             this.brushTempMove = this.brushMoveData[this.datasetSelect];
        //             this.timeMap = this.calcTimeScale(uni_var_data, this.datasetSelect);
        const dataStore = useDataStore();
        dataStore.$subscribe((mutations, state) => {
            if (mutations.events.key == 'system_data') {
                this.smoothSelect = dataStore.smooth;
                this.datasetSelect = dataStore.system_data.file_name;
                let variable_num = parseInt(dataStore.profileData.variable_num);
                let temporal_data = JSON.parse(dataStore.system_data.temporal_data);
                // console.log(temporal_data)
                let res_data = this.dataConvert(temporal_data);
                // console.log(this.dataSelect);
                [this.overview_line_data, this.featureSet, this.dataSet, this.allFeatureSet, this.allData] = this.calcOverviewTimeLine(res_data, variable_num == 1 ? this.smoothSelect : 0);
                // // console.log(this.overview_line_data, this.featureSet, this.dataSet);
                this.brushTempMove = this.brushMoveData[this.datasetSelect];
                // console.log(this.datasetSelect)
                // console.log(this.brushTempMove, res_data, uni_var_data);
                this.timeMap = this.calcTimeScale(res_data, this.datasetSelect);
            }

            if (mutations.events.key == 'dataSelect') {

                if (dataStore.dataSelect == 'sunspots') {
                    this.datasetSelect = dataStore.dataSelect;
                    this.smoothSelect = dataStore.smooth;

                    [this.overview_line_data, this.featureSet, this.dataSet, this.allFeatureSet, this.allData] = this.calcOverviewTimeLine(uni_var_data, this.smoothSelect);
                    // console.log(this.overview_line_data, this.featureSet, this.dataSet);
                    this.brushTempMove = this.brushMoveData[this.datasetSelect];
                    this.timeMap = this.calcTimeScale(uni_var_data, this.datasetSelect);

                } else {

                    this.datasetSelect = dataStore.dataSelect;
                    [this.overview_line_data, this.featureSet, this.dataSet, this.allFeatureSet, this.allData] = this.calcOverviewTimeLine(multi_var_data, 1);
                    // console.log(this.overview_line_data, this.featureSet, this.dataSet);
                    // this.brushTempMove = this.brushMoveData[this.datasetSelect];
                    // this.timeMap = this.calcTimeScale(multi_var_data, this.datasetSelect);
                }
            } else {
                if (dataStore.selectSmooth.length > 0 && dataStore.rowSelectTag == 1) {
                    // console.log(dataStore.selectSmooth)
                    this.selectSmoothObj = {};
                    this.selectSmoothObj[dataStore.selectSmooth[0]] = 1;
                    this.selectSmoothObj[dataStore.selectSmooth[1]] = 1;
                    if (this.datasetSelect == 'sunspots') {
                        console.log(1111, this.datasetSelect)
                        this.selectSmooth = dataStore.selectSmooth;
                        // console.log(this.selectSmooth);
                        // console.log(this.dataSet)
                        this.overLine = [this.dataSet[this.selectSmooth[0]], this.dataSet[this.selectSmooth[1]]];
                        this.overLinePath = [this.lineGenerateFunc(this.overLine[0]), this.lineGenerateFunc(this.overLine[1])];
                        this.nameLine[1] = this.selectSmooth[0] + ':';
                        this.nameLine[2] = this.selectSmooth[1] + ':';
                        this.showLineLegend = 1;
                    }
                }
                if (dataStore.rowSelectTag == 2) {
                    console.log(dataStore.selectResRow);
                    let st = dataStore.selectResRow.time_index;
                    let pre_data = dataStore.selectResRow.prediction_data;
                    let et = st + pre_data.length - 1;
                    // console.log(this.timeMap)
                    this.brushTempMove = [this.timeFormat(this.timeMap[st], this.datasetSelect), this.timeFormat(this.timeMap[et], this.datasetSelect)];
                    let pre_line = []
                    for (let i = st; i <= et; ++i) {
                        pre_line.push({
                            date: this.timeMap[i],
                            value: pre_data[i - st]
                        })
                    }
                    let columnName = dataStore.selectResRow.smooth;
                    if (this.datasetSelect == 'pm')
                        columnName = columnName + '_' + this.openFeature;
                    this.overLine = [this.allData[columnName], pre_line];
                    // console.log(columnName, this.dataSet)
                    this.overLinePath = [this.lineGenerateFunc(this.overLine[0]), , this.lineGenerateFunc(pre_line)];
                    // , this.lineGenerateFunc(pre_line)
                    // console.log(pre_line, this.overLine, this.overLinePath  , this.lineGenerateFunc(pre_line));
                    this.nameLine[1] = dataStore.selectResRow.smooth + ':';
                    this.nameLine[2] = 'Predict:';
                    this.showLineLegend = 1;
                }
            }
        })
    },
    updated () {
        this.showDetail(this.selectAttribute, '#time_line_legend' + this.selectAttribute)

    }
}
</script>

<style>
.tick text {
    font-family: Avenir, Helvetica, Arial, sans-serif;
}

.title {
    font-family: Avenir, Helvetica, Arial, sans-serif;
}

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

.selection {
    fill: black;
}
</style>
