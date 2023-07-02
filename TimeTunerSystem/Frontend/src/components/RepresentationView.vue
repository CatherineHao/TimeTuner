<!--
 * @Description: Representation View
 * @Author: Qing Shi
 * @Date: 2023-06-29 10:17:17
 * @LastEditors: Qing Shi
 * @LastEditTime: 2023-07-01 22:45:59
-->
<template>
    <div class="frameworkTitle" style="padding-right: 10px;">
        <div class="title">Representation View</div>
        <p class="titleTriangle"></p>
        <div style="float: right; margin-top: 3px;">
    
            <span style="font-size: 15px;">Metric: </span>
            <el-select v-model="heatTag" class="m-2" placeholder="Select" style="width: 150px; margin-right: 10px;">
                <el-option v-for="(item, i) in heatOptions" :key="item" :label="item.label" :value="item.value" />
            </el-select>
            <span style="margin-right: 0px; margin-top: 0px;">
                    <el-button style="height: 30px; margin-right: 0px;" @click="legendStatus">
    
                        <img src="../assets/img/colorLegend.png" alt="" width="20" height="20">
                    </el-button>
                    <el-button style="height: 30px; margin-right: 0px;" @click="setupDrag">
                        <svg t="1680200979207" class="icon" viewBox="0 0 1024 1024" version="1.1"
                            xmlns="http://www.w3.org/2000/svg" p-id="5498" width="20" height="20">
                            <path d="M0 0h1024v1024H0z" fill="#515151" fill-opacity="0" p-id="5499"></path>
                            <path
                                d="M484.124444 561.664a35.043556 35.043556 0 0 1 53.703112 34.702222v309.361778l113.891555-116.963556a33.792 33.792 0 0 1 48.810667-0.284444 36.067556 36.067556 0 0 1 0 50.119111l-165.262222 169.585778a33.223111 33.223111 0 0 1-15.303112 8.760889 32.824889 32.824889 0 0 1-16.896 5.290666h-1.137777a35.043556 35.043556 0 0 1-26.282667-10.524444l-170.552889-175.217778a37.205333 37.205333 0 0 1 0-51.768889 35.043556 35.043556 0 0 1 50.460445 0l112.981333 116.053334v-304.469334a35.043556 35.043556 0 0 1 15.644444-34.702222zM504.263111 1.536c6.257778 0.113778 12.288 1.991111 17.521778 5.461333 5.12 1.592889 9.841778 4.437333 13.653333 8.192l-0.568889 0.284445 165.262223 169.585778a36.181333 36.181333 0 0 1 0 50.062222 33.905778 33.905778 0 0 1-48.924445 0L538.396444 119.409778v308.280889a35.043556 35.043556 0 0 1-34.588444 35.043555 35.043556 35.043556 0 0 1-34.531556-35.498666v-305.493334l-113.834666 117.191111a35.043556 35.043556 0 0 1-50.574222 0 37.489778 37.489778 0 0 1 0-51.768889L475.591111 11.832889a35.043556 35.043556 0 0 1 26.908445-10.353778z"
                                fill="#515151" p-id="5500"></path>
                        </svg>
                    </el-button>
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
        <div ref="DataTransformation" style="height: calc(97% + 0px); width: 100%; margin-top: 0px; overflow-y: auto; overflow-x: hidden;">
            <svg :height="(stripeNum * (elHeight - 5) / 28)" width="100%" transform="translate(0, 0)">
                    <g v-for="(item, i) in heatRectData" cursor="pointer" :key="'heat_g' + i"
                        :transform="translateF(0, item.h * i)" :class="'heat_g' + item.class_name">
                        <rect v-for="(item_h, item_i) in item['heat']" :key="'heat_' + item_i" :x="item_h.x" :y="0"
                            :stroke="item_h.colorMap[heatTag]" :width="item_h.w" :height="item_h.h"
                            :fill="item_h.colorMap[heatTag]" :id="'representation_' + item_h.uid"
                            :class="'representationSkipRect'" :fill-opacity="1">
                        </rect>
                        <rect :id="item.class_name" class="black_select_row" :x="item['heat'][0].x" :y="0"
                            :width="elWidth - 10 - item['heat'][0].x" :height="item['heat'][0].h"
                            :fill="checkSelectStatus(i) == 2 ? 'none' : 'none'" stroke="black" stroke-dasharray="4, 4"
                            :stroke-width="checkSelectStatus(i) == 1 ? 3 : 0" :fill-opacity="checkSelectStatus(i) == 2 ? 0 : 0">
                        </rect>
    
                        <text font-size="14" text-anchor="start" dx="0em" dy="1em" cursor="pointer"
                            @mouseenter="mouseoverRepresentation(item.class_name)" @mouseout="mouseoutRepresentation()"
                            @click="selectRepresentation(i, item.class_name)">
                            {{ item.rawName }}
                        </text>
                    </g>
                    <g id="legend_g" :opacity="legendTag == 1 ? 1 : 0"></g>
    
                </svg>
    
        </div>
        <div ref="RepresentationTimeAxis" style="height: 3%; width: 100%; transform: translate(0px, 0px);">
            <svg width="100%" height="100%">
                    <g id="representationTime"></g>
                </svg>
        </div>
    </div>
</template>

<script>
import { scaleUtc, scaleLinear } from 'd3-scale';
import { axisBottom } from 'd3-axis';
import { interpolateYlOrRd } from 'd3-scale-chromatic';
import { useDataStore } from "../stores/counter";
import { select, selectAll } from 'd3-selection';
import * as vsup from 'vsup';
import { drag } from 'd3-drag';
export default {
    name: 'RV',
    props: [],
    data() {
        return {
            elHeight: 1000,
            elWidth: 1000,
            tlHeight: 100,
            tlWidth: 100,
            heatHeight: 0,
            heatTag: 3,
            selectRepresentationTag: 0,
            heatOptions: [{ label: 'RMSE + CORR.', value: 3 }, { label: 'RMSE', value: 4 }, { label: 'CORR.', value: 5 }],
            heatRectData: [],
            smoothSelect: {},
            skipSelect: {},
            stripeNum: 1,
            dataSelect: 'pm',
            allTimeScale: {
                'sunspots': {
                    start: '1878-01-01',
                    end: '2022-01-01'
                },
                'pm': {
                    start: '2013-01-02 00:00:00',
                    end: '2014-03-31 12:00:00'
                }
            },
            selectRepresentationRow: {
                tag: 0,
                status: []
            },
            cid_index: {},
            legendTag: 0
        }
    },
    methods: {
        /**
         * @description: refresh the Representation View. clear all selections
         * @return {*}
         */
        refresh() {
            this.selectRepresentationRow = {
                tag: 0,
                status: new Array(this.stripeNum).fill(0)
            };
            const dataStore = useDataStore();
            dataStore.selectRowClass = 1;
            selectAll('.corr_cir_out').remove();
            selectAll('.corr_cir').attr('opacity', (d, i) => {
                return d.isShow ? 0 : 1;
            }).attr('fill', (d, i) => {
                return d.fill;
            })
        },
        /**
         * @description: check the status of representations
         * @param {int} num Representation Index
         * @return {*} representation status
         */
        checkSelectStatus: function(num) {
            if (this.selectRepresentationRow.tag == 0)
                return 0;
            if (this.selectRepresentationRow.status[num]) {
                return 1;
            } else {
                return 2;
            }
        },
        /**
         * @description: mouseover a representation
         * @param {*} class_name representation name
         * @return {*}
         */
        mouseoverRepresentation(class_name) {
            if (this.selectRepresentationTag) return;
            select('#' + class_name).attr('stroke-width', 3)
            selectAll('.p_x').attr('opacity', (d, i) => {
                return d.id == num ? 1 : 0;
            })
        },
        /**
         * @description: mouseout a representation
         * @return {*}
         */
        mouseoutRepresentation() {
            if (this.selectRepresentationTag) return;
            selectAll('.' + 'black_select_row').attr('stroke-width', 0)
            selectAll('.p_x').attr('opacity', 1);
        },
        /**
         * @description: select (click) a representation
         * @param {*} num Representation Index
         * @param {*} class_name representation name
         * @return {*}
         */
        selectRepresentation(num, class_name) {
            let tdata = []
            this.selectRepresentationTag = 1;
            // console.log(class_name );
            selectAll('.' + 'black_select_row').attr('stroke-width', 0)
            this.selectRepresentationRow.status[num] = 1;
            this.selectRepresentationRow.tag = 1;
            selectAll('.corr_cir').attr('opacity', (d, i) => {
                if (d.class_name == class_name) {
                    tdata.push(d);
                    // return 0.5;
                }
                return d.isShow ? 0 : 0.3;
            }).attr('fill', (d, i) => {
                return '#d9d9d9';
            })
            const dataStore = useDataStore();
            dataStore.selectRowClass = class_name;
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
                .attr('id', (d, i) => 'corr_c' + d.uid)
                .attr('class', 'corr_cir_out')
                .attr('r', 3.5)
                .attr('stroke', 'black')
                .attr('stroke-width', 0.5)
                .attr('fill', d => d.fill)
                .on('click', (e, d) => {
                    let select_dot = {};
                    select_dot[d.uid] = 1;
                    selectAll('.representationSkipRect').attr('opacity', 0.15).attr('stroke-width', 0);

                    for (let i in select_dot) {
                        select("#representation_" + i).attr('opacity', 1);
                    }
                    let t_data = [{
                        x: d.x,
                        y: d.y,
                        fill: d.fill,
                        uid: d.uid
                    }];
                    selectAll('.corr_cir_single').remove();
                    select('#scatter')
                        .append('g')
                        .selectAll('#res_c')
                        .attr('id', 'res_c')
                        .data(t_data)
                        .enter()
                        .append('circle')
                        .attr('cx', dd => dd.x)
                        .attr('cy', dd => dd.y)
                        .attr('id', (dd, i) => 'corr_cir_single' + dd.uid)
                        .attr('class', 'corr_cir_single')
                        .attr('r', 7)
                        .attr('stroke', 'black')
                        .attr('stroke-width', 2)
                        .attr('fill', dd => dd.fill)
                })
        },
        /**
         * @description: determine whether to show or hide the legend
         * @return {*}
         */
        legendStatus() {
            if (this.legendTag == 0) {
                this.legendTag = 1;
            } else if (this.legendTag == 1) {
                this.legendTag = 0;
            }
        },
        /**
         * @description: set the transformation
         * @param {float} x translate x px
         * @param {float} y translate y px
         * @param {float} deg rotate degrees
         * @return {string} the transformation string
         */
        translate(x, y, deg) {
            return `translate(${x}, ${y}) rotate(${deg})`;
        },
        /**
         * @description: set the transformation
         * @param {float} x translate x px
         * @param {float} y translate y px
         * @return {string} the transformation string
         */
        translateF(x, y) {
            return `translate(${x}, ${y})`;
        },
        /**
         * @description: set up the drag tool
         * @return {*}
         */
        setupDrag() {
            let _this = this;
            for (let i in this.cid_index) {
                let drag_func = drag().on('start', dragS).on('drag', dragged).on('end', dragE);

                function dragS() {}

                function dragE(event) {
                    let nt = Math.floor(event.y / _this.cid_index[i].h);
                    select('.heat_g' + i).attr('transform', _this.translateF(0, (nt) * _this.cid_index[i].h))
                    if (nt != _this.cid_index[i].cnt) {
                        for (let j in _this.cid_index) {
                            if (_this.cid_index[i].cnt < nt && _this.cid_index[j].cnt == nt) {

                                select('.heat_g' + j).attr('transform', _this.translateF(0, (_this.cid_index[j].cnt - 1) * _this.cid_index[j].h))
                                _this.cid_index[j].cnt = _this.cid_index[j].cnt - 1;
                                _this.cid_index[i].cnt = nt;
                            }
                            if (_this.cid_index[i].cnt > nt && _this.cid_index[j].cnt == nt) {

                                select('.heat_g' + j).attr('transform', _this.translateF(0, (_this.cid_index[j].cnt + 1) * _this.cid_index[j].h))
                                _this.cid_index[j].cnt = _this.cid_index[j].cnt + 1;
                                _this.cid_index[i].cnt = nt;
                            }

                        }
                    }
                }

                function dragged(event, d) {
                    select('.heat_g' + i).attr('transform', _this.translateF(0, event.y))
                    let nt = Math.floor(event.y / _this.cid_index[i].h);
                    if (nt != _this.cid_index[i].cnt) {
                        for (let j in _this.cid_index) {
                            if (_this.cid_index[i].cnt < nt && _this.cid_index[j].cnt == nt) {
                                select('.heat_g' + j).attr('transform', _this.translateF(0, (_this.cid_index[j].cnt - 1) * _this.cid_index[j].h))
                                _this.cid_index[j].cnt = _this.cid_index[j].cnt - 1;
                                _this.cid_index[i].cnt = nt;
                            }
                            if (_this.cid_index[i].cnt > nt && _this.cid_index[j].cnt == nt) {
                                select('.heat_g' + j).attr('transform', _this.translateF(0, (_this.cid_index[j].cnt + 1) * _this.cid_index[j].h))
                                _this.cid_index[j].cnt = _this.cid_index[j].cnt + 1;
                                _this.cid_index[i].cnt = nt;
                            }
                        }
                    }
                }
                select('.heat_g' + i).call(drag_func);
            }
        },
        /**
         * @description: calculate the representation results
         * @param {*} data all raw representation data
         * @param {*} width svg width
         * @param {*} height svg height
         * @return {*} representation results
         */
        calcRepresentation(data, width, height) {
            let margin = ({ top: 20, right: 10, bottom: 30, left: 50 });
            let line_height = height / 28;
            let maxRmse = -999999;
            let minRmse = 999999;
            let maxTime = -999999;
            let maxCorr = -999999;
            let minCorr = 999999;
            let lineData = [];
            let cnt_id_cnt = 0;
            for (let i in data) {
                let startPos = 0;
                let tp = [];
                for (let j in data[i]) {
                    tp.push({
                        name: data[i][j].Moving + '/' + data[i][j].SK,
                        id: i,
                        skip: parseInt(data[i][j]['skip']),
                        time: j * parseInt(data[i][j]['skip']) + startPos,
                        errorData: 0,
                        id_cnt: cnt_id_cnt++,
                        uid: data[i][j]['smooth'] + '_' + data[i][j]['skip'] + '_' + j,
                        cid: data[i][j]['smooth'] + '_' + data[i][j]['skip'],
                        rmse: parseFloat(data[i][j]['rmse']),
                        corr: parseFloat(data[i][j]['result_corr'])
                    });
                    maxTime = Math.max(maxTime, (parseInt(j) + 1) * parseInt(data[i][j]['skip']) + startPos);
                    maxRmse = Math.max(maxRmse, parseFloat(data[i][j]['rmse']));
                    minRmse = Math.min(minRmse, parseFloat(data[i][j]['rmse']));
                    maxCorr = Math.max(maxCorr, parseFloat(data[i][j]['result_corr']));
                    if (parseFloat(data[i][j]['result_corr']) != 0)
                        minCorr = Math.min(minCorr, parseFloat(data[i][j]['result_corr']));
                }
                lineData.push(tp);
            }
            let HeatSumData = lineData;
            let rmseScale = scaleLinear([minRmse, maxRmse], [0, 1]);
            let corrScale = scaleLinear([minCorr, maxCorr], [0, 1]);
            let timeScale = scaleLinear([0, maxTime], [margin.left, width - margin.right]);
            let quantization2 = vsup.quantization().branching(2).layers(4).valueDomain([minRmse, maxRmse]).uncertaintyDomain([(maxCorr), minCorr]);
            let heatColor = interpolateYlOrRd
            let heatScale2 = vsup.scale().quantize(quantization2).range(heatColor);
            var legend = vsup.legend.arcmapLegend();
            legend
                .scale(heatScale2)
                .size(160)
                .x(600)
                .y(40)
                .vtitle("RMSE")
                .utitle("CORR.");
            select('#legend_g').append('g')
                .call(legend)

            let res_data = [];

            for (let i in HeatSumData) {
                for (let j in HeatSumData[i]) {
                    HeatSumData[i][j].x = timeScale(HeatSumData[i][j].time);
                    HeatSumData[i][j].w = timeScale(HeatSumData[i][j].skip) - timeScale(0);
                    HeatSumData[i][j].v = rmseScale(HeatSumData[i][j].rmse);
                    HeatSumData[i][j].id_cnt = HeatSumData[i][j].id_cnt;
                    HeatSumData[i][j].h = line_height - 3;
                    HeatSumData[i][j].y = parseInt(HeatSumData[i][j].id) * line_height;
                    HeatSumData[i][j].rmseColor = heatColor(HeatSumData[i][j].v);
                    HeatSumData[i][j].corrColor = heatColor(corrScale(HeatSumData[i][j].corr));
                    HeatSumData[i][j].vsupColor2 = heatScale2((HeatSumData[i][j].rmse), HeatSumData[i][j].corr);
                    HeatSumData[i][j].colorMap = ['grey', 'grey', 'grey', HeatSumData[i][j].vsupColor2, HeatSumData[i][j].rmseColor, HeatSumData[i][j].corrColor];
                }
                res_data.push({
                    class_name: HeatSumData[i][0].cid,
                    h: line_height,
                    heat: HeatSumData[i],
                    rawName: HeatSumData[i][0].name
                })
                this.cid_index[HeatSumData[i][0].cid] = {
                    cnt: res_data.length - 1,
                    h: line_height
                };
            }
            return res_data;
        },
        /**
         * @description: paint the time scale
         * @param {*} timestamp time range of the data
         * @return {*}
         */        
        paintTimeScale(timestamp) {
            let margin = ({ top: 20, right: 10, bottom: 30, left: 50 });
            let timeData = [];
            timeData = [new Date(timestamp.start), new Date(timestamp.end)]
            let timeScale = scaleUtc(timeData, [margin.left, this.tlWidth - margin.right]);
            selectAll('#representationTime_g').remove();
            select('#representationTime').append('g').attr('id', 'representationTime_g').attr('transform', 'translate(0, 1)').call(axisBottom(timeScale).ticks((this.tlWidth - margin.left - margin.right) / 80).tickSizeOuter(0))
        },
        /**
         * @description: data processing
         * @param {*} data
         * @return {*}
         */
        dataDivide(data) {
            let res_data = {};
            for (let i in data) {
                if (typeof res_data[parseInt(data[i].rank)] == 'undefined')
                    res_data[parseInt(data[i].rank)] = [];
                res_data[parseInt(data[i].rank)].push(data[i]);
            }
            let result = [];
            for (let i in res_data) {
                result.push({
                    data: res_data[i],
                    smooth: res_data[i][0]['Moving'],
                    skip: res_data[i][0]['skip']
                });
            }
            return result;
        },
        /**
         * @description: data processing
         * @param {*} data
         * @return {*}
         */
        dataConvert(data) {
            let featureSet = [];
            for (let i in data) {
                featureSet.push(i);
            }
            let res_data = [];
            for (let i in data[featureSet[0]]) {
                let tp = {};
                for (let j in featureSet) {
                    tp[featureSet[j]] = data[featureSet[j]][i];
                }
                res_data.push(tp);
            }
            return res_data;
        }
    },
    created() {},
    mounted() {
        this.elHeight = this.$refs.DataTransformation.offsetHeight - 5;
        this.elWidth = this.$refs.DataTransformation.offsetWidth;
        this.tlHeight = this.$refs.RepresentationTimeAxis.offsetHeight;
        this.tlWidth = this.$refs.RepresentationTimeAxis.offsetWidth;

        const dataStore = useDataStore();

        /**
         * @description: watch the data changes in the store
         * @return {*}
         */        
        dataStore.$subscribe((mutations, state) => {
            if (mutations.events.key == 'system_data') {
                this.smoothSelect = dataStore.smooth;
                this.skipSelect = dataStore.skip;
                this.dataSelect = dataStore.system_data.file_name;
                let result_data = JSON.parse(dataStore.system_data.result_data);
                let res_data = this.dataDivide(this.dataConvert(result_data));
                let selectDataSet = [];
                for (let i in res_data) {
                    if (this.smoothSelect[res_data[i].smooth] == 1 && this.skipSelect[res_data[i].skip] == 1) {
                        selectDataSet.push(res_data[i].data);
                    }
                }
                this.stripeNum = selectDataSet.length;
                this.paintTimeScale(this.allTimeScale[this.dataSelect])

                this.heatRectData = this.calcRepresentation(selectDataSet, this.elWidth, this.elHeight);
            }
        })

    },
}
</script>

<style>
.el-input__inner {
    font-family: Avenir, Helvetica, Arial, sans-serif;
}

#DataTransformation {
    font-size: 20px;
}

.el-table .el-table__cell {
    padding: 0px;
}

.selection {
    fill-opacity: 0.2;
}

.el-button {
    /* border: 0px; */
    padding-left: 3px;
    padding-right: 3px;
}

.representationTime_g {
    font-size: 14px;
}

.tick {
    font-size: 14px;
}
</style>
