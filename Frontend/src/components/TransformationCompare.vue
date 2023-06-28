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
 * @Author: Qing Shi
 * @LastEditTime: 2023-06-16 13:21:44
-->
<!--
 * @Description: 
 * @Author: Qing Shi
 * @Date: 2023-01-10 21:20:01
 * @LastEditTime: 2023-03-13 11:47:05
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
                        <svg t="1680200979207" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="5498" width="20" height="20"><path d="M0 0h1024v1024H0z" fill="#515151" fill-opacity="0" p-id="5499"></path><path d="M484.124444 561.664a35.043556 35.043556 0 0 1 53.703112 34.702222v309.361778l113.891555-116.963556a33.792 33.792 0 0 1 48.810667-0.284444 36.067556 36.067556 0 0 1 0 50.119111l-165.262222 169.585778a33.223111 33.223111 0 0 1-15.303112 8.760889 32.824889 32.824889 0 0 1-16.896 5.290666h-1.137777a35.043556 35.043556 0 0 1-26.282667-10.524444l-170.552889-175.217778a37.205333 37.205333 0 0 1 0-51.768889 35.043556 35.043556 0 0 1 50.460445 0l112.981333 116.053334v-304.469334a35.043556 35.043556 0 0 1 15.644444-34.702222zM504.263111 1.536c6.257778 0.113778 12.288 1.991111 17.521778 5.461333 5.12 1.592889 9.841778 4.437333 13.653333 8.192l-0.568889 0.284445 165.262223 169.585778a36.181333 36.181333 0 0 1 0 50.062222 33.905778 33.905778 0 0 1-48.924445 0L538.396444 119.409778v308.280889a35.043556 35.043556 0 0 1-34.588444 35.043555 35.043556 35.043556 0 0 1-34.531556-35.498666v-305.493334l-113.834666 117.191111a35.043556 35.043556 0 0 1-50.574222 0 37.489778 37.489778 0 0 1 0-51.768889L475.591111 11.832889a35.043556 35.043556 0 0 1 26.908445-10.353778z" fill="#515151" p-id="5500"></path></svg>
                    </el-button>
                                            <el-button style="height: 30px;" @click="refresh()">
                                                
                                                <svg t="1680060651492" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2903" width="20" height="20"><path d="M810.666667 273.706667L750.293333 213.333333 512 451.626667 273.706667 213.333333 213.333333 273.706667 451.626667 512 213.333333 750.293333 273.706667 810.666667 512 572.373333 750.293333 810.666667 810.666667 750.293333 572.373333 512z" p-id="2904" fill="#606266"></path></svg>
                                            </el-button>
                                        </span>
        </div>
    </div>
    <div class="frameworkBody">
        <div ref="DataTransformation" style="height: calc(97% + 0px); width: 100%; margin-top: 0px; overflow-y: auto; overflow-x: hidden;">
            <svg :height="(stripNum * (elHeight - 5) / 28)" width="100%" transform="translate(0, 0)">
                                                    <g v-for="(item, i) in heatRectData" cursor="pointer" :key="'heat_g' + i" :transform="translateF(0, item.h * i)" :class="'heat_g' + item.class_name">
                
                                                        <!-- @mouseenter="selectFile(item.class_name)" @mouseout="cancelFile(item.class_name)" @click="clickFile(i, item.class_name)" -->
                                                        <rect v-for="(item_h, item_i) in item['heat']" :key="'heat_' + item_i" :x="item_h.x" :y="0" :stroke="item_h.colorMap[heatTag]"
                                                            :width="item_h.w" :height="item_h.h" :fill="item_h.colorMap[heatTag]" :id="'representation_' + item_h.uid"
                                                            :class="'representationSkipRect'" :fill-opacity="1">
                                                        </rect>
                                                        <!-- <rect v-for="(item_h, item_i) in item['res']" :key="'heat_' + item_i" :x="item_h.x" :y="0"
                                                            :width="item_h.w" :height="item_h.h" :fill="'orange'" :id="'tsr' + item_i"
                                                            :fill-opacity="item_h.fill_opacity">
                                                        </rect> -->
                                                        <rect :id="item.class_name" class="black_select_row" :x="item['heat'][0].x" :y="0" :width="elWidth - 10 - item['heat'][0].x"
                                                            :height="item['heat'][0].h" :fill="checkSelectStatus(i) == 2 ? 'none' : 'none'" stroke="black" stroke-dasharray="4, 4" :stroke-width="checkSelectStatus(i) == 1 ? 3 : 0" :fill-opacity="checkSelectStatus(i) == 2 ? 0 : 0"></rect>
                                    
                                                        <text font-size="14" text-anchor="start" dx="0em" dy="1em" cursor="pointer" @mouseenter="selectFile(item.class_name)" @mouseout="cancelFile(item.class_name)" @click="clickFile(i, item.class_name)">{{
                                                            filename[dataSelect][i].smooth + '/Sk-' + filename[dataSelect][i].skip
                                                        }}</text>
                                                    </g>
                                                    <g id="legend_g" :opacity="legendTag == 1 ? 1 : 0"></g>
                                                    <!-- <g v-for="(item, i) in heatRectData" :key="'heat_g' + i" :transform="translate(0, item.h * i, 0)">
                                                        <rect :id="item.class_name" class="black_select_row" :x="item['heat'][0].x" :y="0" :width="elWidth - 10 - item['heat'][0].x"
                                                            :height="item['heat'][0].h" :fill="checkSelectStatus(i) == 2 ? 'none' : 'none'" stroke="black" :stroke-width="checkSelectStatus(i) == 1 ? 3 : 0" :fill-opacity="checkSelectStatus(i) == 2 ? 0 : 0"></rect>
                                                    </g> -->
                                                    <g v-for="(item, i) in coverRect" :key="'heat_g' + i"
                                                        :transform="translate(0, item.realH, 0)">
                                                        <rect :id="'rst' + i" class="rst" :x="item.x" :y="0" :width="item.w" :height="item.h" :fill="item.colorMap[heatTag]"
                                                            stroke="none" stroke-width="0"></rect>
                                                    </g>
                                                    <!-- <g v-for="(item, i) in groupPath" :key="'group_g' + i" :transform="translate(0, 0, 0)">
                                                        <path :d="'M ' + item.x1 + ' ' + item.y1 + ' L ' + item.x2 + ' ' + item.y2" fill="none" stroke="black">
                                                        </path>
                                                </g> -->
                                    
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
// import res_data from '../assets/model_skip_results.json';

import { arc, curveBumpY, line } from 'd3-shape';
import { scaleUtc, scaleLinear, scaleOrdinal } from 'd3-scale';
import { axisLeft, axisBottom } from 'd3-axis';
import { interpolateRdBu, interpolateYlOrRd, schemeYlOrRd } from 'd3-scale-chromatic';
import { useDataStore } from "../stores/counter";
// import SN_raw_data from "../assets/SN_m_tot_V2.0.csv";
import { select, selectAll } from 'd3-selection';
import { extent, max, min, sum } from 'd3-array';
import { brushX } from 'd3-brush';
import * as vsup from 'vsup';


import d0 from '../assets/allData/univariate_data/single27/rawdata_skip1_0.8.csv';
import d1 from '../assets/allData/univariate_data/single27/rawdata_skip3_0.8.csv';
import d2 from '../assets/allData/univariate_data/single27/rawdata_skip6_0.8.csv';
import d3 from '../assets/allData/univariate_data/single27/rawdata_skip13_0.8.csv';
import d4 from '../assets/allData/univariate_data/single27/rolling3_skip1_0.8.csv';
import d5 from '../assets/allData/univariate_data/single27/rolling3_skip3_0.8.csv';
import d6 from '../assets/allData/univariate_data/single27/rolling3_skip6_0.8.csv';
import d7 from '../assets/allData/univariate_data/single27/rolling3_skip13_0.8.csv';
import d8 from '../assets/allData/univariate_data/single27/rolling6_skip1_0.8.csv';
import d9 from '../assets/allData/univariate_data/single27/rolling6_skip3_0.8.csv';
import d10 from '../assets/allData/univariate_data/single27/rolling6_skip6_0.8.csv';
import d11 from '../assets/allData/univariate_data/single27/rolling6_skip13_0.8.csv';
import d12 from '../assets/allData/univariate_data/single27/rolling13_skip1_0.8.csv';
import d13 from '../assets/allData/univariate_data/single27/rolling13_skip3_0.8.csv';
import d14 from '../assets/allData/univariate_data/single27/rolling13_skip6_0.8.csv';
import d15 from '../assets/allData/univariate_data/single27/rolling13_skip13_0.8.csv';
import d16 from '../assets/allData/univariate_data/single27/weighted3_skip1_0.8.csv';
import d17 from '../assets/allData/univariate_data/single27/weighted3_skip3_0.8.csv';
import d18 from '../assets/allData/univariate_data/single27/weighted3_skip6_0.8.csv';
import d19 from '../assets/allData/univariate_data/single27/weighted3_skip13_0.8.csv';
import d20 from '../assets/allData/univariate_data/single27/weighted6_skip1_0.8.csv';
import d21 from '../assets/allData/univariate_data/single27/weighted6_skip3_0.8.csv';
import d22 from '../assets/allData/univariate_data/single27/weighted6_skip6_0.8.csv';
import d23 from '../assets/allData/univariate_data/single27/weighted6_skip13_0.8.csv';
import d24 from '../assets/allData/univariate_data/single27/weighted13_skip1_0.8.csv';
import d25 from '../assets/allData/univariate_data/single27/weighted13_skip3_0.8.csv';
import d26 from '../assets/allData/univariate_data/single27/weighted13_skip6_0.8.csv';
import d27 from '../assets/allData/univariate_data/single27/weighted13_skip13_0.8.csv';


// multivariate
import m0 from '../assets/allData/multivariate_data/new_res_data/rawdata_skip1.csv';
import m1 from '../assets/allData/multivariate_data/new_res_data/rawdata_skip6.csv';
import m2 from '../assets/allData/multivariate_data/new_res_data/rawdata_skip12.csv';
import m3 from '../assets/allData/multivariate_data/new_res_data/rawdata_skip24.csv';
import m4 from '../assets/allData/multivariate_data/new_res_data/rolling6_skip1.csv';
import m5 from '../assets/allData/multivariate_data/new_res_data/rolling6_skip6.csv';
import m6 from '../assets/allData/multivariate_data/new_res_data/rolling6_skip12.csv';
import m7 from '../assets/allData/multivariate_data/new_res_data/rolling6_skip24.csv';
import m8 from '../assets/allData/multivariate_data/new_res_data/rolling12_skip1.csv';
import m9 from '../assets/allData/multivariate_data/new_res_data/rolling12_skip6.csv';
import m10 from '../assets/allData/multivariate_data/new_res_data/rolling12_skip12.csv';
import m11 from '../assets/allData/multivariate_data/new_res_data/rolling12_skip24.csv';
import m12 from '../assets/allData/multivariate_data/new_res_data/rolling24_skip1.csv';
import m13 from '../assets/allData/multivariate_data/new_res_data/rolling24_skip6.csv';
import m14 from '../assets/allData/multivariate_data/new_res_data/rolling24_skip12.csv';
import m15 from '../assets/allData/multivariate_data/new_res_data/rolling24_skip24.csv';
import m16 from '../assets/allData/multivariate_data/new_res_data/weighted6_skip1.csv';
import m17 from '../assets/allData/multivariate_data/new_res_data/weighted6_skip6.csv';
import m18 from '../assets/allData/multivariate_data/new_res_data/weighted6_skip12.csv';
import m19 from '../assets/allData/multivariate_data/new_res_data/weighted6_skip24.csv';
import m20 from '../assets/allData/multivariate_data/new_res_data/weighted12_skip1.csv';
import m21 from '../assets/allData/multivariate_data/new_res_data/weighted12_skip6.csv';
import m22 from '../assets/allData/multivariate_data/new_res_data/weighted12_skip12.csv';
import m23 from '../assets/allData/multivariate_data/new_res_data/weighted12_skip24.csv';
import m24 from '../assets/allData/multivariate_data/new_res_data/weighted24_skip1.csv';
import m25 from '../assets/allData/multivariate_data/new_res_data/weighted24_skip6.csv';
import m26 from '../assets/allData/multivariate_data/new_res_data/weighted24_skip12.csv';
import m27 from '../assets/allData/multivariate_data/new_res_data/weighted24_skip24.csv';
import { drag } from 'd3-drag';


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
            clickFileTag: 0,
            heatOptions: [{ label: 'RMSE + CORR.', value: 3 }, { label: 'RMSE', value: 4 }, { label: 'CORR.', value: 5 }],
            sample: ['10-slice', '7-slice', '3-slice'],
            smooth: ['Raw Sequence', 'N-Average', 'EMA/Holt'],
            sparkboxData: [],
            heatRectData: [],
            lineData: [],
            smoothLineData: [],
            smoothSelect: {},
            skipSelect: {},
            skiplength: [13, 1, 3, 6, 13, 1, 3, 6, 13, 1, 3, 6, 13, 1, 3, 6, 13, 1, 3, 6, 13, 1, 3, 6, 13, 1, 3, 6, 13, 1, 3, 6, 13, 1, 3, 6],
            heat_set: [],
            columnData: ['Smooth', 'Skip', 'Train-Loss', 'Test-Loss', 'ACF', 'Window Performance'],
            stripNum: 1,
            selectFileName: [],
            filename: {
                'sunspots': [{ smooth: 'RAW', skip: '1' },
                    { smooth: 'RAW', skip: '3' },
                    { smooth: 'RAW', skip: '6' },
                    { smooth: 'RAW', skip: '13' },
                    { smooth: 'MA-3', skip: '1' },
                    { smooth: 'MA-3', skip: '3' },
                    { smooth: 'MA-3', skip: '6' },
                    { smooth: 'MA-3', skip: '13' },
                    { smooth: 'MA-6', skip: '1' },
                    { smooth: 'MA-6', skip: '3' },
                    { smooth: 'MA-6', skip: '6' },
                    { smooth: 'MA-6', skip: '13' },
                    { smooth: 'MA-13', skip: '1' },
                    { smooth: 'MA-13', skip: '3' },
                    { smooth: 'MA-13', skip: '6' },
                    { smooth: 'MA-13', skip: '13' },
                    { smooth: 'WMA-3', skip: '1' },
                    { smooth: 'WMA-3', skip: '3' },
                    { smooth: 'WMA-3', skip: '6' },
                    { smooth: 'WMA-3', skip: '13' },
                    { smooth: 'WMA-6', skip: '1' },
                    { smooth: 'WMA-6', skip: '3' },
                    { smooth: 'WMA-6', skip: '6' },
                    { smooth: 'WMA-6', skip: '13' },
                    { smooth: 'WMA-13', skip: '1' },
                    { smooth: 'WMA-13', skip: '3' },
                    { smooth: 'WMA-13', skip: '6' },
                    { smooth: 'WMA-13', skip: '13' }
                ],
                'pm': [{ smooth: 'RAW', skip: '1' },
                    { smooth: 'RAW', skip: '6' },
                    { smooth: 'RAW', skip: '12' },
                    { smooth: 'RAW', skip: '24' },
                    { smooth: 'MA-6', skip: '1' },
                    { smooth: 'MA-6', skip: '6' },
                    { smooth: 'MA-6', skip: '12' },
                    { smooth: 'MA-6', skip: '24' },
                    { smooth: 'MA-12', skip: '1' },
                    { smooth: 'MA-12', skip: '6' },
                    { smooth: 'MA-12', skip: '12' },
                    { smooth: 'MA-12', skip: '24' },
                    { smooth: 'MA-24', skip: '1' },
                    { smooth: 'MA-24', skip: '6' },
                    { smooth: 'MA-24', skip: '12' },
                    { smooth: 'MA-24', skip: '24' },
                    { smooth: 'WMA-6', skip: '1' },
                    { smooth: 'WMA-6', skip: '6' },
                    { smooth: 'WMA-6', skip: '12' },
                    { smooth: 'WMA-6', skip: '24' },
                    { smooth: 'WMA-12', skip: '1' },
                    { smooth: 'WMA-12', skip: '6' },
                    { smooth: 'WMA-12', skip: '12' },
                    { smooth: 'WMA-12', skip: '24' },
                    { smooth: 'WMA-24', skip: '1' },
                    { smooth: 'WMA-24', skip: '6' },
                    { smooth: 'WMA-24', skip: '12' },
                    { smooth: 'WMA-24', skip: '24' }
                ]
            },
            coverRect: [],
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
                'sunspots': {
                    tag: 0,
                    status: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                },
                'pm': {
                    tag: 0,
                    status: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                }
            },
            selectDot: {
                tag: 0,
                data: []
            },
            cid_index: {},
            legendTag: 0
        }
    },
    methods: {
        refresh() {
            this.selectRepresentationRow = {
                'sunspots': {
                    tag: 0,
                    status: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                },
                'pm': {
                    tag: 0,
                    status: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                }
            };
            this.coverRect = [];
            const dataStore = useDataStore();
            // dataStore.selectRepresentation.data = {};
            // dataStore.selectRepresentation.tag = !dataStore.selectRepresentation.tag;

            dataStore.selectRowClass = 1;

            selectAll('.corr_cir_out').remove();
            selectAll('.corr_cir').attr('opacity', (d, i) => {
                return d.isShow ? 0 : 1;
            }).attr('fill', (d, i) => {
                // if (d.class_name == this.filename[num].substring(0, this.filename[num].length - 8)) return 'orange';
                // else 
                return d.fill;
            })
        },
        checkSelectStatus: function(num) {
            if (this.selectRepresentationRow[this.dataSelect].tag == 0)
                return 0;
            if (this.selectRepresentationRow[this.dataSelect].status[num]) {
                return 1;
            } else {
                return 2;
            }
        },
        selectFile(class_name) {
            if (this.clickFileTag) return;
            select('#' + class_name).attr('stroke-width', 3)
            // .attr('fill', '#777').attr('fill-opacity', 0.5);
            selectAll('.p_x').attr('opacity', (d, i) => {
                return d.id == num ? 1 : 0;
            })
        },
        clickFile(num, class_name) {
            let tdata = []
            this.clickFileTag = 1;
            // console.log(class_name );
            selectAll('.' + 'black_select_row').attr('stroke-width', 0)
            this.selectRepresentationRow[this.dataSelect].status[num] = 1;
            this.selectRepresentationRow[this.dataSelect].tag = 1;
            selectAll('.corr_cir').attr('opacity', (d, i) => {

                if (d.class_name == class_name) {
                    tdata.push(d);
                    // return 0.5;
                }
                return d.isShow ? 0 : 0.3;
            }).attr('fill', (d, i) => {
                // if (d.class_name == this.filename[num].substring(0, this.filename[num].length - 8)) return 'orange';
                // else 
                return '#d9d9d9';
            })
            // console.log(tdata)
            // let select_dot = {};
            // // console.log(this.heatRectData[num]);
            // for (let i in this.heatRectData[num].heat) {
            //     select_dot[this.heatRectData[num].heat[i]['uid']] = 1;
            // }
            // console.log(select_dot);
            const dataStore = useDataStore();
            // dataStore.selectRepresentation.data = select_dot;
            // dataStore.selectRepresentation.tag = !dataStore.selectRepresentation.tag;
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
                    console.log(d)
                    let select_dot = {};
                    select_dot[d.uid] = 1;
                    selectAll('.representationSkipRect').attr('opacity', 0.15).attr('stroke-width', 0);

                    for (let i in select_dot) {
                        // console.log(i);
                        select("#representation_" + i).attr('opacity', 1)
                        // .attr('stroke', 'black').attr('stroke-width', 3);
                    }
                    let _this = this;
                    // _this.tableData = _this.calcTableData(_this.dataSet, select_dot);
                    // _this.tableData = []
                    // console.log(_this.tableData);
                    let t_data = [{
                        x: d.x,
                        y: d.y,
                        fill: d.fill,
                        uid: d.uid
                    }];
                    selectAll('.corr_cir_single').remove();
                    console.log(d.uid)

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

        legendStatus() {
            if (this.legendTag == 0) {
                this.legendTag = 1;
            } else if (this.legendTag == 1) {
                this.legendTag = 0;
            }
        },
        cancelFile(class_name) {
            if (this.clickFileTag) return;
            selectAll('.' + 'black_select_row').attr('stroke-width', 0)
            selectAll('.p_x').attr('opacity', 1)
            // selectAll('.corr_cir').attr('opacity', (d, i) => {
            //     // if (d.class_name == this.filename[num].substring(0, this.filename[num].length - 8)) {
            //     //     return 1;
            //     // }
            //     return 1;
            // })
        },
        translate(x, y, deg) {
            return `translate(${x}, ${y}) rotate(${deg})`;
        },
        translateF(x, y) {
            return `translate(${x}, ${y})`;
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
            let x = scaleLinear()
                .domain([0, max(data, d => parseInt(d.id))])
                .range([margin.left, width - margin.right])

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
                    .attr("d", 'M 0 ' + (-focusHeight / 2 + 30) + ' L 0 ' + (focusHeight / 2 - 30) + 'L 5 ' + (focusHeight / 2 - 30) + ' L 5 ' + (-focusHeight / 2 + 30) + ' Z'),
                )
                .attr("display", s === null ? "none" : null)
                .attr("transform", s === null ? null : (d, i) => `translate(${s[i]},${radius + margin.top})`)

            function brushStart() {
                selectAll('.sparkbox').remove();
            }

            function brushEnd({ selection }) {
                // _this.calcSparkBox(SN_raw_data, _this.tlHeight, _this.tlWidth);
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
                select('#focusLine_g').append('g').attr('id', 'axsg').attr("transform", "translate(0, -25)").call(axisBottom(tScale));

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
                select('#focusLine_g').append('g').attr('id', 'axsg').attr("transform", "translate(0, -25)").call(axisBottom(tScale));

                // _this.timeAxis = xAxis;

                let lineGenerate = line()
                    .x(d => _this.xScale(d.id))
                    .y(d => _this.yScale(d.value));

                _this.select_time_step = timeStep;

                select('#time_path_raw').attr('d', lineGenerate(_this.lineData));
                if (_this.smoothTag) {

                    select('#time_path_selected').attr('d', lineGenerate(_this.smoothLineData));
                }

                select("#selected_area").attr('d', 'M ' + parseInt(selection[0]) + ' ' + 460 + ' L ' + parseInt(selection[1]) + ' ' + 460 + ' L ' + (_this.elWidth - margin.right) + ' 415 L 50 415 Z')
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
        setupDrag() {
            let _this = this;
            for (let i in this.cid_index) {
                let drag_func = drag().on('start', dragS).on('drag', dragged).on('end', dragE);

                function dragS() {

                    console.log('222')
                }

                function dragE(event) {
                    let nt = Math.floor(event.y / _this.cid_index[i].h);
                    select('.heat_g' + i).attr('transform', _this.translateF(0, (nt) * _this.cid_index[i].h))
                    // let nt = Math.floor(event.y / _this.cid_index[i].h);
                    if (nt != _this.cid_index[i].cnt) {
                        for (let j in _this.cid_index) {
                            // if(j == i) continue;
                            if (_this.cid_index[i].cnt < nt && _this.cid_index[j].cnt == nt) {

                                select('.heat_g' + j).attr('transform', _this.translateF(0, (_this.cid_index[j].cnt - 1) * _this.cid_index[j].h))
                                _this.cid_index[j].cnt = _this.cid_index[j].cnt - 1;
                                _this.cid_index[i].cnt = nt;
                                // break;
                            }
                            if (_this.cid_index[i].cnt > nt && _this.cid_index[j].cnt == nt) {

                                select('.heat_g' + j).attr('transform', _this.translateF(0, (_this.cid_index[j].cnt + 1) * _this.cid_index[j].h))
                                _this.cid_index[j].cnt = _this.cid_index[j].cnt + 1;
                                _this.cid_index[i].cnt = nt;
                                // break;
                            }

                        }
                    }
                }

                function dragged(event, d) {
                    // console.log(event, d)
                    select('.heat_g' + i).attr('transform', _this.translateF(0, event.y))
                    let nt = Math.floor(event.y / _this.cid_index[i].h);
                    if (nt != _this.cid_index[i].cnt) {
                        for (let j in _this.cid_index) {
                            // if(j == i) continue;
                            if (_this.cid_index[i].cnt < nt && _this.cid_index[j].cnt == nt) {

                                select('.heat_g' + j).attr('transform', _this.translateF(0, (_this.cid_index[j].cnt - 1) * _this.cid_index[j].h))
                                _this.cid_index[j].cnt = _this.cid_index[j].cnt - 1;
                                _this.cid_index[i].cnt = nt;
                                // break;
                            }
                            if (_this.cid_index[i].cnt > nt && _this.cid_index[j].cnt == nt) {

                                select('.heat_g' + j).attr('transform', _this.translateF(0, (_this.cid_index[j].cnt + 1) * _this.cid_index[j].h))
                                _this.cid_index[j].cnt = _this.cid_index[j].cnt + 1;
                                _this.cid_index[i].cnt = nt;
                                // break;
                            }

                        }
                    }
                }
                select('.heat_g' + i).call(drag_func);
            }
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
                let skipLength = this.skiplength[parseInt(kk)];
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
                    //     skip: this.skiplength[i],
                    //     time: j * this.skiplength[i] + startPos,
                    //     rmse: parseFloat(data[i][j]['rmse'])
                    // });
                    tp.push({
                        id: i,
                        skip: this.skiplength[i],
                        time: j * this.skiplength[i] + startPos,
                        errorData: 0,
                        rmse: parseFloat(data[i][j]['rmse']),
                        corr: parseFloat(data[i][j]['result_corr'])
                    });
                    // console.log(data[i][j]['129_pearson'])
                    maxTime = Math.max(maxTime, j * this.skiplength[i] + startPos);
                    maxRmse = Math.max(maxRmse, parseFloat(data[i][j]['rmse']));
                    minRmse = Math.min(minRmse, parseFloat(data[i][j]['rmse']));
                    maxCorr = Math.max(maxCorr, parseFloat(data[i][j]['result_corr']));
                    if (parseFloat(data[i][j]['result_corr']) != 0)
                        minCorr = Math.min(minCorr, parseFloat(data[i][j]['result_corr']));
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
        calcRMSEHeatMultiVariable(data, width, height) {
            let margin = ({ top: 20, right: 10, bottom: 30, left: 50 });
            // let sdata = [];
            let line_height = height / 28;


            let allStrip = data.length;
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

            let lineData = [];
            let cnt_id_cnt = 0;
            for (let i in data) {
                // console.log(data[i])
                let startPos = 0;
                let tp = [];
                for (let j in data[i]) {
                    tp.push({
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
                    // console.log(data[i][j]['129_pearson'])
                    maxTime = Math.max(maxTime, (parseInt(j) + 1) * parseInt(data[i][j]['skip']) + startPos);
                    maxRmse = Math.max(maxRmse, parseFloat(data[i][j]['rmse']));
                    minRmse = Math.min(minRmse, parseFloat(data[i][j]['rmse']));
                    maxCorr = Math.max(maxCorr, parseFloat(data[i][j]['result_corr']));
                    if (parseFloat(data[i][j]['result_corr']) != 0)
                        minCorr = Math.min(minCorr, parseFloat(data[i][j]['result_corr']));
                }
                lineData.push(tp);
            }
            let HeatSumData = [];
            for (let i = 0; i < lineData.length; ++i) {
                HeatSumData.push(lineData[i]);
            }

            let rmseScale = scaleLinear([minRmse, maxRmse], [0, 1]);
            let corrScale = scaleLinear([minCorr, maxCorr], [0, 1]);
            let timeScale = scaleLinear([0, maxTime], [margin.left, width - margin.right]);
            let quantization2 = vsup.quantization().branching(2).layers(4).valueDomain([minRmse, maxRmse]).uncertaintyDomain([(maxCorr), minCorr]);

            // let heatColor = interpolateYlOrRd;
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
                    HeatSumData[i][j].allH = line_height;
                    HeatSumData[i][j].realH = line_height * i;
                    HeatSumData[i][j].y = parseInt(HeatSumData[i][j].id) * line_height;
                    HeatSumData[i][j].rmseColor = heatColor(HeatSumData[i][j].v);
                    HeatSumData[i][j].corrColor = heatColor(corrScale(HeatSumData[i][j].corr));
                    HeatSumData[i][j].vsupColor2 = heatScale2((HeatSumData[i][j].rmse), HeatSumData[i][j].corr);
                    HeatSumData[i][j].colorMap = ['grey', 'grey', 'grey', HeatSumData[i][j].vsupColor2, HeatSumData[i][j].rmseColor, HeatSumData[i][j].corrColor];
                }
                // HeatSumData[i].sort((a, b) => a.v - b.v)
                res_data.push({
                    class_name: HeatSumData[i][0].cid,
                    h: line_height,
                    heat: HeatSumData[i]
                })
                this.cid_index[HeatSumData[i][0].cid] = {
                    cnt: res_data.length - 1,
                    h: line_height
                };
            }
            // console.log(res_data);
            console.log(this.cid_index)
            return res_data;
        },
        calcRMSETempHeatMultiVariate(data, smooth_data, width, height) {
            let margin = ({ top: 20, right: 20, bottom: 30, left: 50 });
            // let sdata = [];
            let allStrip = data.length;
            let line_height = height / 10;
            let maxRmse = -999999;
            let minRmse = 999999;
            let maxTime = -999999;
            let maxTemp = -999999;
            let minTemp = 999999;
            let maxCorr = -999999;
            let minCorr = 999999;
            let heatDataSet = [];
            let heatBeforeDataSet = [];
            let id_cnt = 0;

            let lineData = [];
            // console.log(smooth_data)
            let cnt_id_cnt = 0;
            for (let i in data) {
                let startPos = 0;
                let tp = [];
                for (let j in data[i]) {
                    let startTemp = j * parseInt(data[i][j]['skip']) + startPos;
                    let aveTemp = sum(smooth_data[i].slice(startTemp + 24, startTemp + 24 + 12), d => parseFloat(d.temp)) / 12;
                    // console.log(startTemp, smooth_data[i], smooth_data[i].slice(startTemp + 24, startTemp + 24 +  12))
                    // break

                    tp.push({
                        id: i,
                        skip: parseInt(data[i][j]['skip']),
                        time: j * parseInt(data[i][j]['skip']) + startPos,
                        errorData: 0,
                        id_cnt: cnt_id_cnt++,
                        aveTemp: aveTemp,
                        rmse: parseFloat(data[i][j]['rmse']),
                        corr: parseFloat(data[i][j]['result_corr'])
                    });
                    // console.log(data[i][j]['129_pearson'])
                    maxTime = Math.max(maxTime, (j) * parseInt(data[i][j]['skip']) + startPos);
                    maxRmse = Math.max(maxRmse, parseFloat(data[i][j]['rmse']));
                    minRmse = Math.min(minRmse, parseFloat(data[i][j]['rmse']));
                    maxCorr = Math.max(maxCorr, parseFloat(data[i][j]['result_corr']));
                    // if (parseFloat(data[i][j]['result_corr']) != 0)
                    minCorr = Math.min(minCorr, parseFloat(data[i][j]['result_corr']));
                    minTemp = Math.min(minTemp, aveTemp);
                    maxTemp = Math.max(maxTemp, aveTemp);
                }
                lineData.push(tp);
            }
            let HeatSumData = [];
            for (let i = 0; i < lineData.length; ++i) {
                HeatSumData.push(lineData[i]);
            }

            let rmseScale = scaleLinear([minRmse, maxRmse], [0, 1]);
            // let errorScale = scaleLinear([minError, maxError], [0, 1]);
            let tempScale = scaleLinear([minTemp, maxTemp], [0, 1]);
            let corrScale = scaleLinear([minCorr, maxCorr], [0, 1]);
            let timeScale = scaleLinear([0, maxTime], [margin.left, width - margin.right]);
            let quantization1 = vsup.quantization().branching(2).layers(4).valueDomain([165, 188]).uncertaintyDomain([(300), 295]);
            let quantization2 = vsup.quantization().branching(2).layers(4).valueDomain([minRmse, maxRmse]).uncertaintyDomain([(maxCorr), minCorr]);

            let heatColor = interpolateYlOrRd;
            let heatScale1 = vsup.scale().quantize(quantization1).range(heatColor);
            let heatScale2 = vsup.scale().quantize(quantization2).range(heatColor);

            var legend = vsup.legend.arcmapLegend();

            legend
                .scale(heatScale1)
                .size(160)
                .x(200)
                .y(100)
                .vtitle("RMSE")
                .utitle("Temp");
            select('#legend_g').append('g')
                .call(legend)
            let res_data = [];
            for (let i in HeatSumData) {
                console.log(HeatSumData[i])
                for (let j in HeatSumData[i]) {
                    // console.log(lineData[i][j].skip)
                    // console.log(timeScale(HeatSumData[i][j].skip), timeScale(HeatSumData[i][j].time), maxTime)
                    HeatSumData[i][j].x = timeScale(HeatSumData[i][j].time);
                    HeatSumData[i][j].w = timeScale(HeatSumData[i][j].skip) - timeScale(0);
                    HeatSumData[i][j].v = rmseScale(HeatSumData[i][j].rmse);
                    HeatSumData[i][j].id_cnt = HeatSumData[i][j].id_cnt;
                    HeatSumData[i][j].h = height / 28 - 3
                    HeatSumData[i][j].y = parseInt(HeatSumData[i][j].id) * line_height;
                    HeatSumData[i][j].rmseColor = heatColor(HeatSumData[i][j].v);
                    // HeatSumData[i][j].errorColor = heatColor(errorScale(HeatSumData[i][j].errorData));
                    // HeatSumData[i][j].rawColor = heatColor(rawScale(HeatSumData[i][j].rawData));
                    HeatSumData[i][j].corrColor = heatColor(corrScale(HeatSumData[i][j].corr));
                    HeatSumData[i][j].vsupColor1 = heatScale1(HeatSumData[i].rmse, HeatSumData[i][j].aveTemp);
                    // HeatSumData[i][j].vsupColor1 = heatScale1((HeatSumData[i][j].errorData), (HeatSumData[i][j].rawData));
                    HeatSumData[i][j].vsupColor2 = heatScale2((HeatSumData[i][j].rmse), HeatSumData[i][j].corr);
                    HeatSumData[i][j].colorMap = ['grey', 'grey', 'grey', HeatSumData[i][j].vsupColor2, HeatSumData[i][j].rmseColor, HeatSumData[i][j].corrColor];
                    // if (j == 10)
                    // break
                }
                res_data.push({
                    h: line_height,
                    heat: HeatSumData[i]
                })
                // break
            }
            // console.log(res_data)
            return res_data;
        },
        paintTimeScale: function(timestamp) {
            let margin = ({ top: 20, right: 10, bottom: 30, left: 50 });
            let timeData = [];
            timeData = [new Date(timestamp.start), new Date(timestamp.end)]
            let timeScale = scaleUtc(timeData, [margin.left, this.tlWidth - margin.right]);
            // this.timeScaleGlobal = timeScale;
            selectAll('#representationTime_g').remove();
            select('#representationTime').append('g').attr('id', 'representationTime_g').attr('transform', 'translate(0, 1)')
                .call(axisBottom(timeScale).ticks((this.tlWidth - margin.left - margin.right) / 80).tickSizeOuter(0))
        }
    },
    created() {},
    mounted() {
        this.elHeight = this.$refs.DataTransformation.offsetHeight - 5;
        this.elWidth = this.$refs.DataTransformation.offsetWidth;
        this.tlHeight = this.$refs.RepresentationTimeAxis.offsetHeight;
        this.tlWidth = this.$refs.RepresentationTimeAxis.offsetWidth;
        // this.dataSelect = 'sunspots'

        // this.paintTimeScale(this.allTimeScale[this.dataSelect])

        const dataStore = useDataStore();
        let _this = this;
        let dataSet = [d0, d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13, d14, d15, d16, d17, d18, d19, d20, d21, d22, d23, d24, d25, d26, d27];
        this.stripNum = dataSet.length;
        
        let dataSet2 = [m0, m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13, m14, m15, m16, m17, m18, m19, m20, m21, m22, m23, m24, m25, m26, m27];

        // console.log(this.heatRectData);

        // this.heatRectData = this.calcRMSEHeatMultiVariable(dataSet, this.elWidth, this.elHeight);


                    // this.dataSelect = 'sunspots'

                    // this.paintTimeScale(this.allTimeScale[this.dataSelect])

                    // this.heatRectData = this.calcRMSEHeatMultiVariable(dataSet, this.elWidth, this.elHeight - 5);


        dataStore.$subscribe((mutations, state) => {
            if (mutations.events.key == 'dataSelect') {

                if (dataStore.dataSelect == 'sunspots') {
                    this.dataSelect = 'sunspots'
                    this.smoothSelect = dataStore.smooth;
                    this.skipSelect = dataStore.skip;
                    let selectDataSet = [];
                    this.selectFileName = [];
                    for (let i in dataSet) {
                        if (this.smoothSelect[this.filename[this.dataSelect][i].smooth] == 1 && this.skipSelect[this.filename[this.dataSelect][i].skip] == 1) {
                            selectDataSet.push(dataSet[i]);
                            this.selectFileName.push(this.filename[this.dataSelect][i]);
                        }
                    }

                    this.paintTimeScale(this.allTimeScale[this.dataSelect])

                    this.heatRectData = this.calcRMSEHeatMultiVariable(selectDataSet, this.elWidth, this.elHeight);

                } else {
                    // console.log(111111)
                    this.dataSelect = 'pm'
                    this.smoothSelect = dataStore.smooth;
                    this.skipSelect = dataStore.skip;
                    let selectDataSet = [];
                    this.selectFileName = [];
                    for (let i in dataSet2) {
                        if (this.smoothSelect[this.filename[this.dataSelect][i].smooth] == 1 && this.skipSelect[this.filename[this.dataSelect][i].skip] == 1) {
                            selectDataSet.push(dataSet2[i]);
                            this.selectFileName.push(this.filename[this.dataSelect][i]);
                            console.log(this.filename[this.dataSelect][i].smooth, this.filename[this.dataSelect][i].skip)
                        }
                    }

                    this.paintTimeScale(this.allTimeScale[this.dataSelect])

                    this.heatRectData = this.calcRMSEHeatMultiVariable(selectDataSet, this.elWidth, this.elHeight);
                }
            }
            // if (dataStore.dataSelect == 'sunspots') {
            //     let dataSet = [d0, d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13, d14, d15, d16, d17, d18, d19, d20, d21, d22, d23, d24, d25, d26, d27, d28, d29, d30, d31, d32, d33, d34, d35];
            //     // console.log(dataSet);
            //     this.heatRectData = this.calcRMSEHeatMultiVariable(dataSet, this.elWidth, this.elHeight);
            // } else {
            //     let dataSet = [m0, m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13, m14, m15, m16, m17, m18, m19, m20, m21, m22, m23, m24, m25, m26, m27];
            //     // console.log(dataSet);
            //     this.heatRectData = this.calcRMSEHeatMultiVariable(dataSet, this.elWidth, this.elHeight);
            // }

            // if (this.selectDot.tag != dataStore.selectDot.tag) {
            //     this.selectDot.tag = dataStore.selectDot.tag;
            //     this.selectDot.data = dataStore.selectDot.data;
            //     let coverRect = [];
            //     for (let i in this.heatRectData) {
            //         for (let j in this.heatRectData[i].heat) {
            //             if (this.selectDot.data[this.heatRectData[i].heat[j].uid]) {
            //                 coverRect.push(this.heatRectData[i].heat[j]);
            //             }
            //         }
            //     }
            //     this.coverRect = coverRect;
            // }
            // if (dataStore.selectRowClass != '') {
            //     this.selectRepresentationRow
            // }
            //     selectAll('#tsr_1').attr('opacity', 0);
            //     let coverRect = [];
            //     for (let i in _this.heatRectData) {
            //         for (let j in _this.heatRectData[i].heat) {
            //             // console.log(_this.heatRectData[i][j])

            //             if (dataStore.selectDot[this.heatRectData[i].heat[j].id_cnt] == 1) {
            //                 // select('#tsr' + this.heatRectData[i].heat[j].id_cnt).attr('opacity', 1).attr('stroke', 'blue').attr('stroke-width', 0);
            //                 coverRect.push({
            //                     x: select('#tsr' + this.heatRectData[i].heat[j].id_cnt).attr('x'),
            //                     y: select('#tsr' + this.heatRectData[i].heat[j].id_cnt).attr('y'),
            //                     w: select('#tsr' + this.heatRectData[i].heat[j].id_cnt).attr('width'),
            //                     h: select('#tsr' + this.heatRectData[i].heat[j].id_cnt).attr('height'),
            //                     fill: select('#tsr' + this.heatRectData[i].heat[j].id_cnt).attr('fill'),
            //                     cnt: select('#tsr' + this.heatRectData[i].heat[j].id_cnt).attr('class'),
            //                 })
            //             }
            //             // else select('#tsr' + this.heatRectData[i].heat[j].id_cnt).attr('opacity', 0)
            //             // .attr('fill', '#d9d9d9');
            //         }
            //     }
            //     console.log(coverRect);
            //     this.coverRect = coverRect;
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

.el-input__inner {
    font-family: Avenir, Helvetica, Arial, sans-serif;
}

#DataTransformation {
    font-size: 20px;
    /* font-family: Roboto; */
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
