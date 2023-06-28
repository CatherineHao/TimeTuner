<!--
 * @Description: 
 * @Author: Qing Shi
 * @Date: 2023-01-10 21:20:01
 * @LastEditTime: 2023-02-18 20:36:39
-->
<template>
    <div class="frameworkTitle">
        <div class="title">Model Explainer</div>
        <p class="titleTriangle"></p>
    </div>
    <div class="frameworkBody">
        <!-- <div ref="modelTable"
                                                            style="height: 100%; width: calc(50% - 7.5px + 30px); float: left; overflow:auto; font-size: 18px;">
                                                            <el-table :data="tableData" style="width: 100%" height="100%"
                                                                :header-cell-style="{ 'text-align': 'center', 'font-size': '16px', 'background-color': 'rgba(250, 250, 250, 1)' }"
                                                                :cell-style="{ 'text-align': 'center', 'background-color': 'rgba(250, 250, 250, 1)', 'font-size': '16px' }">
                                                                <el-table-column type="expand">
                                                                    <template #default="props">
                                                                        <div m="4">
                                                                            <el-table :data="props.row['sub_slice']" stripe style="width: 100%; float: right;"
                                                                                height="200" :table-layout="'auto'" :header-cell-style="{ 'text-align': 'center' }"
                                                                                :cell-style="{ 'text-align': 'center' }">
                                                                                <el-table-column label="ID" prop="slice_num" />
                                                                                <el-table-column label="MAE" prop="MAE" />
                                                                                <el-table-column label="STD" prop="STD" />
                                                                                <el-table-column label="MEAN" prop="Mean" />
                                                                                <el-table-column label="BEGIN" prop="train_begin" />
                                                                                <el-table-column label="END" prop="test_end" />

                                                                            </el-table>
                                                                        </div>
                                                                    </template>
                                                                </el-table-column>
                                                                <el-table-column label="Slice number" prop="slice_number" />
                                                                <el-table-column label="Smooth" prop="smooth" />
                                                            </el-table>
                                                        </div> -->
        <div ref="modelExplainer" style="height: 100%; width: calc(100%); float: left;">
            <svg id="modelExplainer" height="100%" width="100%">

                <g>
                    <text v-if="runTag" font-weight="bold" x="15" y="15" font-size="20">Validation Loss</text>
                    <text v-if="runTag" font-weight="bold" :x="elWidth - 125" :y="elHeight - 35" font-size="20">Train
                        Loss</text>
                    <g v-for="(item, i) in xAxis">
                        <path :d="'M ' + item.x + ' ' + item.y + ' L ' + + item.x + ' ' + (item.y - 5)" stroke="black">
                        </path>
                        <path :d="'M ' + item.x + ' ' + item.y + ' L ' + + item.x + ' ' + (20)" stroke="rgba(229, 229, 229)"
                            stroke-dasharray="0"></path>
                        <text :x="item.x" :y="elHeight - 10" dx="-0em" text-anchor="middle">{{ item.t }}</text>
                    </g>
                    <g v-for="(item, i) in yAxis">
                        <path :d="'M ' + (item.x + 25) + ' ' + item.y + ' L ' + + (item.x + 30) + ' ' + (item.y)"
                            stroke="black"></path>
                        <path :d="'M ' + (elWidth - 20) + ' ' + item.y + ' L ' + + (item.x + 30) + ' ' + (item.y)"
                            stroke="rgba(229, 229, 229)" stroke-dasharray="0"></path>
                        <text :x="0" :y="item.y" dy="0.3em">{{ item.t }}</text>
                    </g>
                </g>
                <g>
                    <g v-for="(item, i) in nodeData" :key="'tag_' + i" :id="item.cnt + '_' + item.cnt1">
                        <circle v-if="item.cnt1 == 0" :cx="item.x" :cy="item.y" :r="8" :fill="item.color"
                            stroke="black"
                            :opacity="select1[item.cnt] == 1 && select2[item.cnt1] == 1 ? 1 : 0"
                            @mouseover="selectD(item.data)" @mouseout="cancelD()"></circle>

                        <path v-else-if="item.cnt1 == 1"  d="M -8 8 L 0 -8 L 8 8 Z"
                            :transform="translate(item.x, item.y, 0)" :fill="item.color" stroke="black"
                            :opacity="select1[item.cnt] == 1 && select2[item.cnt1] == 1 ? 1 : 0"
                            @mouseover="selectD(item.data)" @mouseout="cancelD()"></path>
                        <rect v-else-if="item.cnt1 == 2"  :transform="translate(item.x, item.y, 0)" x="-8" y="-8"
                            height="16" width="16" :fill="item.color" stroke="black"
                            :opacity="select1[item.cnt] == 1 && select2[item.cnt1] == 1 ? 1 : 0"
                            @mouseover="selectD(item.data)" @mouseout="cancelD()"></rect>
                        <g v-else :transform="translate(item.x, item.y, 0)"
                            :opacity="select1[item.cnt] == 1 && select2[item.cnt1] == 1 ? 1 : 0"
                            @mouseover="selectD(item.data)" @mouseout="cancelD()">
                            <path d="M -8 -8 L 8 8" :stroke="item.color" stroke-width="3"></path>
                            <path d="M -8 8 L 8 -8" :stroke="item.color" stroke-width="3"></path>
                        </g>
                    </g>
                </g>
                <g :transform="translate(elWidth, 10, 0)">
                    <g>
                        <text x="3" y="3">input_shape: {{ selectData["input_shape"] }}</text>
                        <text x="3" y="23">output_shape: {{ selectData["output_shape"] }}</text>
                        <text x="3" y="43">skip: {{ selectData["skip"] }}</text>
                        <text x="3" y="63">result numbers: {{ selectData["result numbers"] }}</text>
                        <text x="3" y="83">loss=mean_squared_error: {{
                            parseFloat(selectData["loss=mean_squared_error"]).toFixed(5) }}</text>
                        <text x="3" y="103">val_loss=val_mse: {{ parseFloat(selectData["val_loss=val_mse"]).toFixed(5)
                        }}</text>
                        <text x="3" y="123">file_name: {{ selectData["file_name"] }}</text>
                    </g>
                    <g :transform="translate(0, 200, 0)">
                        <g v-for="(item, i) in colormap" :transform="translate(5, i * 30, 0)"
                            @click="select1[i] = !select1[i]">
                            <rect x="0" y="0" width="40" height="30" stroke="black"
                                :fill="select1[i] == 1 ? item : '#D9D9D9'"></rect>
                            <text x="45" y="20">{{ smoothType[i] }}</text>
                        </g>
                    </g>
                    <g :transform="translate(180, 215, 0)">
                        <g :transform="translate(5, 0, 0)" @click="select2[0] = !select2[0]">
                            <circle cx="0" cy="0" r="8" stroke="black" :fill="select2[0] == 1 ? 'steelblue' : '#D9D9D9'">
                            </circle>
                            <text x="15" y="5">{{ 13 }}</text>
                        </g>
                        <g :transform="translate(5, 30, 0)" @click="select2[1] = !select2[1]">
                            <path d="M -8 8 L 0 -8 L 8 8 Z" stroke="black"
                                :fill="select2[1] == 1 ? 'steelblue' : '#D9D9D9'">
                            </path>
                            <text x="15" y="5">{{ 6 }}</text>
                        </g>
                        <g :transform="translate(5, 60, 0)" @click="select2[2] = !select2[2]">
                            <rect x="-8" y="-8" width="16" height="16" stroke="black"
                                :fill="select2[2] == 1 ? 'steelblue' : '#D9D9D9'"></rect>
                            <text x="15" y="5">{{ 3 }}</text>
                        </g>
                        <g :transform="translate(5, 90, 0)" @click="select2[3] = !select2[3]">
                            <g>
                                <path d="M -8 -8 L 8 8" :stroke="select2[3] == 1 ? 'steelblue' : '#D9D9D9'"
                                    stroke-width="3"></path>
                                <path d="M -8 8 L 8 -8" :stroke="select2[3] == 1 ? 'steelblue' : '#D9D9D9'"
                                    stroke-width="3"></path>
                            </g>
                            <text x="15" y="5">{{ 1 }}</text>
                        </g>
                    </g>
                </g>
            </svg>
        </div>
    </div>
</template>
<script>
import { scaleLinear } from 'd3-scale';
import { useDataStore } from "../stores/counter";
import average6Data from "../assets/average6_slice_info.json";
import { max, min } from 'd3-array';
import res_data from '../assets/data/model_skip_results.json'
export default {
    name: 'modelExplainerView',
    props: ['sliceData'],
    data () {
        return {
            runTag: false,
            elHeight: 0,
            elWidth: 0,
            legendWidth: 0,
            nodeData: [],
            nodeData2: [],
            nodeData3: [],
            nodeData4: [],
            xAxis: [],
            yAxis: [],
            tableData: [],
            selectData: {
                "input_shape": "",
                "output_shape": "",
                "skip": "",
                "result numbers": "",
                "loss=mean_squared_error": "0",
                "val_loss=val_mse": "0",
                "file_name": ""
            },
            colormap: ["#a6cee3",
                "#1f78b4",
                "#b2df8a",
                "#33a02c",
                "#fb9a99",
                "#e31a1c",
                "#fdbf6f",
                "#ff7f00",
                "#cab2d6",
                "#6a3d9a",
                "#b15928"],
            smoothType: ["rawdata", "rolling3", "weighted3", "rolling6", "weighted6", "rolling9", "weighted9", "rolling13", "weighted13", "rolling26", "weighted26"],
            select1: { 0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1 },
            select2: { 0: 1, 1: 1, 2: 1, 3: 1 },
        }
    },
    methods: {
        selectD (d) {
            this.selectData = d;
        },
        cancelD () {
            this.selectData = {
                "input_shape": "",
                "output_shape": "",
                "skip": "",
                "result numbers": "",
                "loss=mean_squared_error": "0",
                "val_loss=val_mse": "0",
                "file_name": ""
            };
        },
        translate (x, y, deg) {
            return `translate(${x}, ${y}) rotate(${deg})`;
        },
        formatNum (num) {
            //1. 可能是字符串，转换为浮点数
            //2. 乘以100 小数点向右移动两位
            //3. Math.round 进行四舍五入
            //4. 除以100 小数点向左移动两位 实现保留小数点后两位
            let v = Math.round(parseFloat(num) * 100) / 100;
            // 去掉小数点 存为数组
            let arrayNum = v.toString().split(".");
            //只有一位（整数）
            if (arrayNum.length == 1) {
                return v.toString() + ".00";
            }
            if (arrayNum.length > 1) {
                //小数点右侧 如果小于两位 则补一个0
                if (arrayNum[1].length < 2) {
                    return v.toString() + "0";
                }
                return v;
            }

        },
        calcAxis (xDRange, yDRange) {
            let xRange = scaleLinear([0, 1], xDRange);
            let yRange = scaleLinear([0, 1], yDRange);
            const xScale = scaleLinear(xDRange, [30, this.elWidth - 20]);
            const yScale = scaleLinear(yDRange, [this.elHeight - 30, 20]);
            let xAxis = [];
            let yAxis = [];
            for (let i = 0; i <= 10; ++i) {
                xAxis.push({
                    t: xRange(i / 10).toFixed(2),
                    x: xScale(xRange(i / 10)),
                    y: this.elHeight - 25,
                    // d: 
                });
                yAxis.push({
                    t: (yRange(i / 10)).toFixed(2),
                    y: yScale(yRange(i / 10)),
                    x: 0
                });
            }
            return [xAxis, yAxis];
        },
        calcNode (data) {

            let nodeData = [];
            const xScale = scaleLinear([min(data, d => d.x), max(data, d => d.x)], [30, this.elWidth - 20]);
            const yScale = scaleLinear([min(data, d => d.y), max(data, d => d.y)], [this.elHeight - 30, 20]);
            for (let i = 0; i < data.length; ++i) {
                let rx = data[i].x;
                let ry = data[i].y;
                nodeData.push({
                    x: xScale(rx),
                    y: yScale(ry),
                    r: [rx, ry],
                    color: data[i].color,
                    cnt: data[i].cnt,
                    cnt1: data[i].cnt1,
                    data: data[i].data
                });
            }
            return nodeData;
        },
        calcTableData (data) {
            let tData = new Array();
            for (const d of data) {
                let td = [];
                for (let i in d['sub slice']) {
                    let tmpD = {}
                    for (let k in d['sub slice'][i]) {
                        let tmp = d['sub slice'][i][k]
                        if (k == "Mean" || k == "STD" || k == 'MAE') {
                            tmp = this.formatNum(tmp);
                        }
                        tmpD[k] = tmp;
                    }
                    td.push(tmpD);
                }
                let tdata = {
                    slice_number: d['slice_info']['slice_number'] + '-slice',
                    smooth: '13-Average',
                    sub_slice: td
                }
                tData.push(tdata);
            }
            return tData;
        }
    },
    created () {
    },
    mounted () {
        this.elHeight = this.$refs.modelExplainer.offsetHeight;
        this.elWidth = this.$refs.modelExplainer.offsetWidth * 0.75;
        this.legendWidth = this.$refs.modelExplainer.offsetWidth * 0.25;
        const dataStore = useDataStore();
        // dataStore.$subscribe((mutation, state) => {
        let nodeData = []
        // console.log(res_data);
        // for (let d of this.sliceData[0]['sub slice']) {
        //     nodeData.push({
        //         color: 'red',
        //         mae: d['MAE'],
        //         acf: d['acf'],
        //         pacf: d['pacf']
        //     })
        // }
        // for (let d of average6Data[0]['sub slice']) {
        //     nodeData.push({
        //         color: 'blue',
        //         mae: d['MAE'],
        //         acf: d['acf'],
        //         pacf: d['pacf']
        //     })
        // }
        let cnt = 0;
        let nodeData2 = [];
        let nodeData3 = [];
        let nodeData4 = [];
        let min_x = 9999;
        let min_y = 9999;
        let max_x = -9999;
        let max_y = -9999;

        for (let d of res_data) {
            let cnt1 = 0;
            for (let t of d['predic_info']) {
                min_x = Math.min(min_x, parseFloat(t['loss=mean_squared_error']));
                max_x = Math.max(max_x, parseFloat(t['loss=mean_squared_error']));
                min_y = Math.min(min_y, parseFloat(t['val_loss=val_mse']));
                max_y = Math.max(max_y, parseFloat(t['val_loss=val_mse']));

                // if (cnt1 == 0) {
                nodeData.push({
                    x: t['loss=mean_squared_error'],
                    y: t['val_loss=val_mse'],
                    color: this.colormap[cnt],
                    cnt: cnt,
                    cnt1: cnt1,
                    data: t
                });

                cnt1++;
            }
            cnt++
        }
        this.runTag = true;
        this.nodeData = this.calcNode(nodeData);
        console.log(this.nodeData);

        // this.nodeData2 = this.calcNode(nodeData2);
        // this.nodeData3 = this.calcNode(nodeData3);
        // this.nodeData4 = this.calcNode(nodeData4);
        [this.xAxis, this.yAxis] = this.calcAxis([min_x, max_x], [min_y, max_y]);
        this.tableData = this.calcTableData(this.sliceData);
        // })

        // this.nodeData = this.calcNode(1);
        // console.log(this.nodeData);
        // [this.xAxis, this.yAxis] = this.calcAxis();
        // this.tableData = this.calcTableData(this.sliceData);

        // console.log(this.tableData);
        // console.log(this.xAxis, this.yAxis)
    },
    watch: {
        select1: {
            handler () {
                let nodeData = [];
                let cnt = 0;
                let min_x = 9999;
                let min_y = 9999;
                let max_x = -9999;
                let max_y = -9999;

                for (let d of res_data) {
                    let cnt1 = 0;
                    for (let t of d['predic_info']) {
                        min_x = Math.min(min_x, parseFloat(t['loss=mean_squared_error']));
                        max_x = Math.max(max_x, parseFloat(t['loss=mean_squared_error']));
                        min_y = Math.min(min_y, parseFloat(t['val_loss=val_mse']));
                        max_y = Math.max(max_y, parseFloat(t['val_loss=val_mse']));

                        // if (cnt1 == 0) {
                        if (this.select1[cnt] == 0 || this.select2[cnt1] == 0) {
                            continue;
                        }
                        nodeData.push({
                            x: t['loss=mean_squared_error'],
                            y: t['val_loss=val_mse'],
                            color: this.colormap[cnt],
                            cnt: cnt,
                            cnt1: cnt1,
                            data: t
                        });

                        cnt1++;
                    }
                    cnt++
                }

                this.nodeData = this.calcNode(nodeData);
                [this.xAxis, this.yAxis] = this.calcAxis([min_x, max_x], [min_y, max_y]);

            },
            deep: true
        },
        select2: {
            handler () {
                let nodeData = [];
                let cnt = 0;
                let min_x = 9999;
                let min_y = 9999;
                let max_x = -9999;
                let max_y = -9999;

                for (let d of res_data) {
                    let cnt1 = 0;
                    for (let t of d['predic_info']) {
                        min_x = Math.min(min_x, parseFloat(t['loss=mean_squared_error']));
                        max_x = Math.max(max_x, parseFloat(t['loss=mean_squared_error']));
                        min_y = Math.min(min_y, parseFloat(t['val_loss=val_mse']));
                        max_y = Math.max(max_y, parseFloat(t['val_loss=val_mse']));

                        // if (cnt1 == 0) {
                        if (this.select1[cnt] == 0 || this.select2[cnt1] == 0) {
                            continue;
                        }
                        nodeData.push({
                            x: t['loss=mean_squared_error'],
                            y: t['val_loss=val_mse'],
                            color: this.colormap[cnt],
                            cnt: cnt,
                            cnt1: cnt1,
                            data: t
                        });

                        cnt1++;
                    }
                    cnt++
                }

                this.nodeData = this.calcNode(nodeData);
                [this.xAxis, this.yAxis] = this.calcAxis([min_x, max_x], [min_y, max_y]);

            },
            deep: true
        }
    }
}
</script>
<style>
*,
*::before,
*::after {
    font-weight: normal;
}

.cell {
    font-weight: normal;
    color: black;
}

/*chrome--------------------------------------------start*/
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

/* Track */
::-webkit-scrollbar-track {
    background: #ffffff;
    border-radius: 8px;
}

/* Handle */
::-webkit-scrollbar-thumb {
    background: rgb(201, 201, 202);
    border-radius: 8px;
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
    background: rgb(162, 162, 163);
}

.el-menu::-webkit-scrollbar,
.el-table__body-wrapper::-webkit-scrollbar {
    display: none;
}

.el-menu:hover::-webkit-scrollbar,
.el-table__body-wrapper:hover::-webkit-scrollbar {
    display: block;
}

/*chrome--------------------------------------------end*/
</style>
