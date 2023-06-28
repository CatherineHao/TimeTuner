<!--
 * @Description: 
 * @Author: Qing Shi
 * @Date: 2023-01-10 21:20:01
 * @LastEditTime: 2023-03-20 02:11:32
-->
<template>
    <div class="frameworkTitle" style="padding-right: 10px;">
        <div class="title">Temporal View</div>
        <p class="titleTriangle"></p>
    </div>
    <div class="frameworkBody">
    
        <div style="height: calc(100%); width: 100%; margin-top: 0px; overflow-y: auto;">
            <!-- <div style="height: 1000px;">
                    
                                </div> -->
            <div style="height: 95%; overflow-y: auto; width: 100%;" ref="timeline">
                <div v-for="(item, i) in overview_line_data" :key="'overview_line_' + i">
                    <div :style="{
                            'background-color': 'white',
                            'margin-top': '3px',
                            'height': item.rowHeight + 'px',
                            }" @click="showDetail(i, '#time_line_legend' + i)">
                        <svg width="100%" :height="item.rowHeight">
                                <clipPath id="clipPathHorizon">
                                                    <rect :x="0" :y="0" :width="tlWidth" :height="30"></rect>
                                            </clipPath>
                                <g clip-path="url(#clipPathHorizon)" :id="'brush_area' + i">
                                    <path :d="item.d" :stroke="'none'" :fill="item.fill[0]" :transform="translate(0, -item.height * 3, 0)"></path>
                                    <path :d="item.d" :stroke="'none'" :fill="item.fill[1]" :transform="translate(0, -item.height * 2, 0)"></path>
                                    <path :d="item.d" :stroke="'none'" :fill="item.fill[2]"  :transform="translate(0, -item.height * 1, 0)"></path>
                                    <path :d="item.d" :stroke="'none'" :fill="item.fill[3]"></path>
                                    <text x="10" y="18">{{ item.feature }}</text>
                                </g>
                                <g :id="'time_line_legend' + i" :transform="translate(0, tlHeight - featureSet.length * 30, 0)"></g>
    
                                <g :id="'time_line' + i" :transform="translate(0, tlHeight - featureSet.length * 30, 0)">
                                    <path :id="'time_path_raw' + i" :d="timeLinePath" :fill="'none'" :stroke="'grey'"></path>
                                </g>
                            </svg>
                    </div>
                </div>
            </div>
        </div>
    
    </div>
</template>

<script>
import { axisBottom, axisLeft } from 'd3-axis';
import { scaleLinear, scaleOrdinal } from 'd3-scale';
import { arc, area, line } from 'd3-shape';
import SN_raw_data from "../assets/SN_m_tot_V2.0.csv";
import multi_var_data from "../assets/15month_result/raw_15month.csv";
import { extent, max, min, sum } from 'd3-array';
import { brushX } from 'd3-brush';
import { select, selectAll, selectorAll } from 'd3-selection';
export default {
    name: 'DataTransformationView',
    props: ['timeData', 'sliceData'],
    data() {
        return {
            horizon_level: 4,
            elHeight: 1000,
            elWidth: 1000,
            tlHeight: 100,
            tlWidth: 100,
            featureSet: [],
            showTag: '',
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
            smoothTag: 0,
            timeLinePath: null,
            linePathTag: 0,
            coverRect: [],
            predict_line: [],
            predict_tag: 0,
            overview_line_data: [],
            horizon_color: ['#c7dbee', '#a1cadf', '#4892c3', '#0e4591'],
            dataSet: []
        }
    },
    methods: {
        showDetail(cnt, id) {
            console.log(id);
            for (let i in this.overview_line_data) {
                if (i == cnt)
                    this.overview_line_data[i].rowHeight = this.tlHeight - this.featureSet.length * 30;
                else
                    this.overview_line_data[i].rowHeight = 30;
            }
            this.calcTimeLine(this.dataSet[this.featureSet[cnt]], this.tlHeight - this.tlHeight - this.featureSet.length * 30 - 40, this.tlWidth, id);
            this.setupBrush(this.dataSet[this.featureSet[cnt]], '#brush_area' + cnt, this.tlWidth, cnt)
        },
        translate(x, y, deg) {
            return `translate(${x}, ${y}) rotate(${deg})`;
        },
        calcSparkBox(data, height) {
            let margin = ({ top: 20, right: 20, bottom: 30, left: 50 });
            // let height = 440;
            // let width = 1000;
            let focusHeight = 100;

            let y = scaleLinear()
                .domain([0, max(data, d => parseFloat(d.value))])
                .range([height - focusHeight - 30 - margin.bottom, margin.top])
            let sBData = [];
            let x = this.xScale;
            let sparkBoxData = [];
            let timeGap = 130
            for (let i = 0; i < data.length; i += timeGap) {
                let tempValue = data.slice(i, i + timeGap).map(d => parseFloat(d.value)).sort((a, b) => a - b)
                let sumData = sum(tempValue);
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
        setupBrush: function(data, id, width, cnt) {
            let focusHeight = 100;
            let margin = ({ top: -20, right: 20, bottom: 50, left: 50 });
            const timeBrush = brushX()
                .extent([
                    [margin.left, 0],
                    [width - margin.right, 30]
                ])
                .on('start', brushStart)
                .on('brush', brushed)
                .on('end', brushEnd);
            this.timeBrush = timeBrush;
            let x = scaleLinear()
                .domain([0, data.length - 1])
                .range([margin.left, width - margin.right])
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
                    .attr("stroke-width", 1)
                    .attr("cursor", "ew-resize")
                    .attr("d", 'M -5 ' + (-focusHeight / 2 + 30) + ' L -5 ' + (focusHeight / 2 - 30) + 'L 5 ' + (focusHeight / 2 - 30) + ' L 5 ' + (-focusHeight / 2 + 30) + ' Z'),
                )
                .attr("display", s === null ? "none" : null)
                .attr("transform", s === null ? null : (d, i) => `translate(${s[i]},${radius + margin.top})`)

            function brushStart() {
                console.log(222)
                selectAll('.sparkbox').remove();
            }

            function brushEnd({ selection }) {
                console.log(111)
                _this.calcSparkBox(SN_raw_data, _this.tlHeight, _this.tlWidth);
                let timeStep = [parseInt(_this.rxScale(selection[0])), parseInt(_this.rxScale(selection[1]))];

                _this.xScale.domain(timeStep);
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
                // selectAll('#axsg').remove();
                // select('#focusLine_g').append('g').attr('id', 'axsg').attr("transform", `translate(0, ${-30})`).call(axisBottom(tScale));

                // _this.timeAxis = xAxis;

                let lineGenerate = line()
                    .x((d) => _this.xScale(d.id))
                    .y(d => _this.yScale(d.value));

                // _this.select_time_step = timeStep;

                select('#time_path_raw' + cnt).attr('d', lineGenerate(_this.lineData));
                // if (_this.smoothTag) {

                //     select('#time_path_selected').attr('d', lineGenerate(_this.smoothLineData));
                // }
            }

            function brushed({ selection }) {
                console.log(selection);
                let timeStep = [parseInt(_this.rxScale(selection[0])), parseInt(_this.rxScale(selection[1]))];
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
                // selectAll('#axsg').remove();
                // select('#focusLine_g').append('g').attr('id', 'axsg').attr("transform", "translate(0, -25)").call(axisBottom(tScale));

                // // _this.timeAxis = xAxis;

                let lineGenerate = line()
                    .x((d) => _this.xScale(d.id))
                    .y(d => _this.yScale(d.value));

                // _this.select_time_step = timeStep;

                select('#time_path_raw' + cnt).attr('d', lineGenerate(_this.lineData));
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
            select(id).call(timeBrush)
                .call(timeBrush.move, [x(988), x(1760)]);

        },
        calcTimeLine(data, height, width, id) {
            console.log(data)
            let margin = ({ top: -20, right: 20, bottom: 50, left: 50 });
            let focusHeight = 100;

            let y = scaleLinear()
                .domain([min(data, d => parseFloat(d.value)), max(data, d => parseFloat(d.value))])
                .range([margin.top, height - margin.bottom])
            let x = scaleLinear()
                .domain([0, max(data, d => parseInt(d.id))])
                .range([margin.left, width - margin.right])
            // let x = scaleLinear([0, data.length - 1], [margin.left, width - margin.right]);
            const rx = scaleLinear()
                .domain([margin.left, width - margin.right])
                .range([0, max(data, d => parseInt(d.id))]);

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
                .x((d, i) => x(d.id))
                .y(d => y(d.value));
            this.lineGenerateFunc = lineGenerate;

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
            selectAll('yAxis_g').remove();
            console.log(id)
            select(id).append('g').attr('id', 'yAxis_g').call(yAxis, y, 'Value');
            this.timeLinePath = lineGenerate(data);

            this.lineData = data;
            // console.log(this.timeLinePath)
        },
        calcMonth(startTime, endTime) {
            let year = parseInt(endTime / 100) - parseInt(startTime / 100);
            let month = endTime % 100 - startTime % 100 + 1;
            let sumMonth = year * 12 + month;
            return sumMonth;
        },
        calcFeatureLine(data, width, height) {
            let margin = { left: 0, right: 0, top: 0, bottom: 0 };
            let xScale = scaleLinear([0, data.length - 1], [margin.left, width - margin.right]);
            let vRange = extent(data, d => parseFloat(d.value));
            let yScale = scaleLinear(vRange, [height - margin.bottom, margin.top]);
            let lineGenerate = line().x((d, i) => xScale(i)).y(d => yScale(parseFloat(d.value)));
            let line_data = lineGenerate(data);
            return line_data;
        },
        calcFeatureArea(data, width, height) {
            let margin = { left: 50, right: 20, top: 0, bottom: 0 };

            let xScale = scaleLinear([0, data.length - 1], [margin.left, width - margin.right]);
            let vRange = extent(data, d => parseFloat(d.value));
            // vRange
            let yScale = scaleLinear(vRange, [this.horizon_level * (height - margin.bottom), margin.top]);
            let areaGenerate = area().x((d, i) => xScale(parseFloat(i))).y0(d => yScale(parseFloat(d.value))).y1(d => yScale(parseFloat(vRange[0])));
            let area_data = areaGenerate(data);
            return area_data;
        },
        calcOverviewTimeLine(data) {
            console.log(data);
            let featureSet = [];
            let allData = {};
            for (let i in data[0]) {
                if (i == 'date' || i == 'id' || i == 'timestamp')
                    continue;
                featureSet.push(i);
                allData[i] = [];
            }
            // featureSet = ['raw']
            // allData['raw'] = []
            for (let i in data) {
                for (const j of featureSet) {
                    // console.log(data[i][j])
                    let v = parseFloat(data[i][j]);
                    if (j == 'wnd_dir')
                        v = (v / 45).toFixed(0)
                    allData[j].push({
                        date: data[i]['id'],
                        value: v,
                        id: parseInt(i)
                    });
                }
            }
            console.log(allData);
            let result_data = new Array();
            // for (let i in allData) {
            //     result_data.push({
            //         d: this.calcFeatureLine(allData[i], this.tlWidth, this.tlHeight / (featureSet.length *2)),
            //         raw: allData[i],
            //         feature: i
            //     })
            // }

            for (let i in allData) {
                result_data.push({
                    d: this.calcFeatureArea(allData[i], this.tlWidth, 30),
                    raw: allData[i],
                    feature: i,
                    fill: this.horizon_color,
                    height: 30,
                    rowHeight: 30
                })
            }
            // console.log(result_data);

            return [result_data, featureSet, allData];
        }
    },
    created() {},
    mounted() {
        this.tlHeight = this.$refs.timeline.offsetHeight * 1;
        this.tlWidth = this.$refs.timeline.offsetWidth;
        // console.log(SN_raw_data)
        // this.dataSet = multi_var_data;


        [this.overview_line_data, this.featureSet, this.dataSet] = this.calcOverviewTimeLine(SN_raw_data);
        // console.log(this.dataSet);
        this.showDetail(0, '#time_line_legend0')
    },
}
</script>

<style>
*,
*::before,
*::after {
    font-weight: normal;
}

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
