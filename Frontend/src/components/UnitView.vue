<!--
 * @Description: 
 * @Author: Qing Shi
 * @Date: 2023-01-10 21:20:01
 * @LastEditTime: 2023-06-21 09:38:19
-->
<template>
    <div class="frameworkTitle">
        <div class="title">Variable Inspector View</div>
        <p class="titleTriangle"></p>
        <span v-if="dataName != ''" style="position: absolute; top: 5px; right: 20px; font-size: 18px; font-size: 15px;">
            {{ dataName }} <span v-if="dataName == 'PM 2.5'">(mg/m<sup>3</sup>)</span> : &nbsp; <span
                style="position: absolute; top: 20px; left: 100px;">{{ valueRange[0] }}</span> <img
                src="../assets/img/blues2.png" alt="" width="150" height="16"><span
                style="position: absolute; top: 20px; left: 245px;">{{ valueRange[1] }}</span>
        </span>
    </div>
    <div class="frameworkBody">
        <div ref="DistributionView" style="height: 100%; width: 100%;">
            <!-- <img src="../assets/img/a.png" alt="" style="height: 100%;"> -->

            <svg id="distributionSVG" height="100%" width="100%">
                <!-- <g>
                                    <g v-for="(item, i) in sparkBoxData" :key="'box' + i">
                                        <rect x="10" y="10" fill="red"></rect>
                                        <rect :x="item.rect1.x" :y="item.rect1.y" :width="item.rect1.w" :height="item.rect1.h"
                                            fill="#f2f5fa">
                                        </rect>
                                        <rect :x="item.rect2.x" :y="item.rect2.y" :width="item.rect2.w" :height="item.rect2.h"
                                            fill="#dce3f3">
                                        </rect>
                                        <path :d="'M ' + item.line.x1 + ' ' + item.line.y + ' L ' + item.line.x2 + ' ' + item.line.y"
                                            :fill="'none'" :stroke="'#6d70b6'" stroke-width="3"></path>
                                    </g>
                                <g>
                                    <path :d="linePath" stroke="steelblue" fill="none"></path>
                                </g>
                            </g> -->

                <!-- <g>
                                <g>
                                        <text v-for="(o, i) in SS_name" :key="'F_leg' + i" :x="0" :y="0" text-anchor="end"
                                            :transform="translate(40, 50 + i * (elHeight - 30) / S_name.length, -65)">{{
                                                (o).charAt(0).toUpperCase() + (o).slice(1) }}</text>
                                    </g>
                                    <g>
                                        <text v-for="(o, i) in SS_name" :key="'F_leg' + i" :x="0" :y="0"
                                            :transform="translate(50 + (elWidth - 50) / S_name.length / 2 + (elWidth - 50) / S_name.length * i, (elHeight - 30) + 20, 0)"
                                            font-weight="100" text-anchor="middle">{{ (o).charAt(0).toUpperCase() + (o).slice(1) }}</text>
                                    </g>
                                    <g v-for="(o, i) in F_sparkBoxData" :key="'fsb' + i" :transform="translate(o.tx, o.ty, 0)">
                                        <g :transform="translate(50, 15, 0)">
                                            <rect v-for="(oo, r_i) in o.boxData" :key="'fsbr' + r_i" :x="oo.x" :y="oo.y" :width="oo.w"
                                                :height="oo.h" :fill="oo.fillColor" :opacity="oo.fill" stroke="white"></rect>
                                        </g>
                                        <rect :x="o.rx" :y="o.ry" :width="o.w" :height="o.h" fill="none" stroke="black"></rect>
                                    </g>
                                    </g> -->
                <g>
                    <g>
                        <text v-for="(o, i) in show_name" :key="'F_leg' + i" :x="0" :y="0" text-anchor="end" :font-size="14"
                            :transform="translate(37, 35 + i * (elHeight - 30) / show_name.length, -60)">{{
                                nameMap[dataSelect][o] }}</text>
                    </g>
                    <g>
                        <text v-for="(o, i) in show_name" :key="'F_leg' + i" :x="0" :y="0" :font-size="14"
                            :transform="translate(40 + (elWidth - 40) / show_name.length / 2 + (elWidth - 40) / show_name.length * i, (elHeight - 30) + 25, 0)"
                            font-weight="100" text-anchor="middle">{{
                                nameMap[dataSelect][o] }}</text>
                    </g>
                    <g v-for="(o, i) in F_sparkBoxData" :key="'fsb' + i" :transform="translate(o.tx, o.ty, 0)">
                        <g :transform="translate(40, 2, 0)">
                            <rect v-for="(oo, r_i) in o.boxData" :key="'fsbr' + r_i" :x="oo.x" :y="oo.y" :width="oo.w"
                                :height="oo.h" :fill="oo.fillColor" :opacity="oo.fill" stroke="white"></rect>
                        </g>
                        <rect :x="o.rx" :y="o.ry" :width="o.w" :height="o.h" :class="'unitRect'" :id="'unit' + i"
                            fill="black" stroke="#304051" fill-opacity="0" stroke-width="0.7"
                            @mouseenter="mouseoverFeature(o.boxData, o.nameX, o.nameY, o.nameXr, o.nameYr, i)"
                            @mouseout="mouseoutFeature()" @click="clickFeature(o.nameXr, o.nameYr)"></rect>
                    </g>
                </g>
                <g>
                    <g :transform="translate(elWidth * 2 / 3 - 25, 15, 0)" id="mouseRect"
                        :opacity="selectTag == 1 ? 1 : 0">

                        <rect v-for="(oo, r_i) in selectRect.data" :key="'fsbr' + r_i" :x="oo.mouseX" :y="oo.mouseY"
                            :width="oo.mouseW" :height="oo.mouseH" :fill="oo.fillColor" :opacity="oo.fill" stroke="white">
                        </rect>

                        <rect :x="0" :y="0" :width="elWidth / 3 + 20" :height="elWidth / 3 + 20" :fill="'none'"
                            stroke="black"></rect>
                        <text font-size="14" :x="(elWidth / 3 + 20) / 2" :y="elWidth / 3 + 20 + 40"
                            text-anchor="middle">{{ selectRect.nameX }}</text>

                        <text font-size="14" :transform="translate(-20, (elWidth / 3 + 20) / 2, -60)"
                            text-anchor="end">{{ selectRect.nameY }}</text>
                    </g>
                </g>
            </svg>
        </div>
    </div>
</template>

<script>
import { max, min, sum } from "d3-array";
import { axisBottom, axisLeft } from "d3-axis";
import { scaleLinear, scaleOrdinal } from "d3-scale";
import { select, selectAll } from "d3-selection";
import { line } from "d3-shape";
import uni_data from "../assets/allData/univariate_data/all_smooth_value.csv";
import multi_data from "../assets/allData/multivariate_data/used_multi.csv";
import { interpolateYlGnBu } from "d3-scale-chromatic";
import { useDataStore } from "../stores/counter";
export default {
    name: 'UnitView',
    props: [],
    data () {
        return {
            elHeight: 0,
            elWidth: 0,
            sparkBoxData: [],
            F_sparkBoxData: [],
            linePath: null,
            F_name: ['pm25', 'temp', 'rh', 'psfc', 'wnd_dir', 'wnd_spd'],
            S_name: ['raw', 'rolling3', 'rolling6', 'rolling13', 'weighted3', 'weighted6', 'weighted13'],

            SS_name: ['RAW', 'MA-3', 'MA-6', 'MA-13', 'WMA-3', 'WMA-6', 'WMA-13'],
            show_name: [],
            tfData: [],
            dataName: '',
            valueRange: [],
            selectRect: [],
            selectTag: 0,
            dataSelect: 'pm',
            smoothSelect: {},
            nameMap: {
                'sunspots': {
                    'raw': 'RAW',
                    'rolling3': 'MA-3',
                    'rolling6': 'MA-6',
                    'rolling9': 'MA-9',
                    'rolling13': 'MA-13',
                    'weighted3': 'WMA-3',
                    'weighted6': 'WMA-6',
                    'weighted9': 'WMA-9',
                    'weighted13': 'WMA-13',
                },
                'pm': {
                    'pm25': 'PM2.5',
                    'temp': 'temp',
                    'rh': 'rh',
                    'psfc': 'psfc',
                    'wnd_dir': 'wnd_dir',
                    'wnd_spd': 'wnd_spd'
                }
            }
        }
    },
    methods: {

        translate (x, y, deg) {
            return `translate(${x}, ${y}) rotate(${deg})`;
        },
        mouseoverFeature (data, nameX, nameY, nameXr, nameYr, num) {
            // console.log(data);
            selectAll('.unitRect').attr('stroke-width', 1);
            select('#unit' + num).attr('stroke-width', 3);
            this.selectTag = 1;
            let xScale = scaleLinear(data[0].xRange, [0, this.elWidth / 3 + 20]);
            let yScale = scaleLinear(data[0].yRange, [this.elWidth / 3 + 20, 0]);
            let x = scaleLinear(data[0].xDomain, [0, this.elWidth / 3 + 20]);
            let y = scaleLinear(data[0].yDomain, [this.elWidth / 3 + 20, 0]);
            selectAll('#feature_axis_g').remove();
            select('#mouseRect').append('g').attr('id', 'feature_axis_g').attr('transform', `translate(0, ${this.elWidth / 3 + 20})`).call(axisBottom(x).ticks(4).tickSizeOuter(0));
            select('#mouseRect').append('g').attr('id', 'feature_axis_g').call(axisLeft(y).ticks(4).tickSizeOuter(0));
            for (let i in data) {
                data[i].mouseX = xScale(data[i].x);
                data[i].mouseY = yScale(data[i].y);
                data[i].mouseW = xScale(data[i].w);
                data[i].mouseH = yScale(data[i].h);
            }
            this.selectRect = {
                data: data,
                nameX: nameX,
                nameY: nameY,
                nameXr: nameXr,
                nameYr: nameYr
            };
        },
        mouseoutFeature: function () {
            this.selectTag = 0;

            selectAll('.unitRect').attr('stroke-width', 1);
        },
        clickFeature: function (nameXr, nameYr) {
            const dataStore = useDataStore();
            dataStore.rowSelectTag = 1;
            dataStore.selectSmooth = [nameXr, nameYr];
        },
        calcSparkBox (data, height, width) {
            let margin = ({ top: 10, right: 30, bottom: 20, left: 30 });
            // let height = 440;
            // let width = 1000;
            let focusHeight = 0;

            let y = scaleLinear()
                .domain([0, max(data, d => parseFloat(d.value))])
                .range([height - margin.bottom, height - margin.bottom - (width - margin.left - margin.right)]);
            let y2 = scaleLinear()
                .domain([0, max(data, d => parseFloat(d.value))])
                .range([focusHeight, margin.top])
            let x = scaleLinear()
                .domain([0, max(data, d => (parseInt(d.id)))])
                .range([margin.left, width - margin.right])
            let sparkBoxData = [];
            let lineData = [];
            let timeData = [];
            let lenData = [];
            for (let i = 0; i < data.length; ++i) {
                lineData.push({
                    id: parseInt(data[i].id),
                    v: parseFloat(data[i].value)
                });
                if (i == 0 || i == data.length - 1 || i % Math.floor(data.length / 10) === 0) {
                    lenData.push(x(parseInt(data[i].id)));
                    timeData.push(parseInt(data[i].timestamp));
                }
            }
            let timeScale = scaleOrdinal(timeData, lenData);
            let lineGenerate = line().x(d => x(d.id)).y(d => y(d.v));
            // console.log(timeData);
            select('#distributionSVG').append('g').call(axisBottom(timeScale)).attr('transform', `translate(${0}, ${this.elHeight - margin.bottom})`);
            select('#distributionSVG').append('g').call(axisLeft(y)).attr('transform', `translate(${margin.left}, ${0})`);

            for (let i = 0; i < data.length; i += Math.round(data.length / 20)) {
                // let tempValue = Array.from(new Set(data.slice(i, i + 10).map(d => parseFloat(d.value)).sort((a, b) => a - b)));
                let tempValue = data.slice(i, i + Math.round(data.length / 20)).map(d => parseFloat(d.value)).sort((a, b) => a - b)
                let sumData = sum(tempValue);

                // console.log(sumData)

                // console.log(tempValue[tempValue.length /2 - 1], tempValue.length /2 - 1);
                sparkBoxData.push({
                    rect1: {
                        x: x(parseInt(data[i].id)),
                        y: y(tempValue[tempValue.length - 1]),
                        w: Math.abs(x(parseInt(data[i + ((i + Math.round(data.length / 20) < data.length) ? Math.round(data.length / 20) : (data.length - 1 - i))].id)) - x(parseInt(data[i].id))),
                        h: Math.abs(y(tempValue[0]) - y(tempValue[tempValue.length - 1]))
                    },
                    rect2: {
                        x: x(parseInt(data[i].id)),
                        y: y(tempValue[parseInt(tempValue.length * 3 / 4) - 1]),
                        w: Math.abs(x(parseInt(data[i + ((i + Math.round(data.length / 20) < data.length) ? Math.round(data.length / 20) : (data.length - 1 - i))].id)) - x(parseInt(data[i].id))),
                        h: Math.abs(y(tempValue[parseInt(tempValue.length * 3 / 4) - 1]) - y(tempValue[parseInt(tempValue.length / 4) - 1]))
                    },
                    line: {
                        x1: x(parseInt(data[i].id)),
                        // y: y(tempValue[parseInt(tempValue.length /2) - 1]),
                        // y: y((tempValue[0] + tempValue[parseInt(tempValue.length - 1)]) / 2),
                        y: y(sumData / tempValue.length),
                        x2: Math.abs(x(parseInt(data[i + ((i + Math.round(data.length / 20) < data.length) ? Math.round(data.length / 20) : (data.length - 1 - i))].id)) - x(parseInt(data[i].id))) + x(parseInt(data[i].id))
                    }
                })
            }
            // console.log(sparkBoxData)
            return [sparkBoxData, lineGenerate(lineData)];
        },

        calcDisSparkBox (data, height, width, box_num, F1_name, F2_name, Val_name) {
            // console.log(Val_name, F1_name, F2_name)
            let margin = ({ top: 0, right: 0, bottom: 0, left: 0 });

            let y = scaleLinear()
                .domain([min(data, d => parseFloat(d[F2_name])), max(data, d => parseFloat(d[F2_name]))])
                .range([height - margin.bottom, margin.top])
            let x = scaleLinear()
                .domain([min(data, d => parseFloat(d[F1_name])), max(data, d => parseFloat(d[F1_name]))])
                .range([margin.left, width - margin.right])
            let xx = scaleLinear()
                .domain([0, box_num])
                .range([margin.left, width - margin.right])

            let sparkBoxData = [];
            let timeGap = {};
            let timeG = (x.domain()[1] - x.domain()[0]) / (box_num);
            let valG = (y.domain()[1] - y.domain()[0]) / (box_num);
            for (let i = 0; i < data.length; ++i) {
                // console.log(data[i], data[i][F1_name], data[i][F2_name])
                let tx = Math.floor((data[i][F1_name] - x.domain()[0]) / timeG);
                if (tx == box_num) tx--;
                let ty = Math.floor((data[i][F2_name] - y.domain()[0]) / valG);
                if (ty == box_num) ty--;
                // console.log(tx, ty)
                if (typeof timeGap[tx] === 'undefined') {
                    timeGap[tx] = {};
                }
                if (typeof timeGap[tx][ty] === 'undefined') {
                    timeGap[tx][ty] = [];
                }
                timeGap[tx][ty].push(data[i]);
            }
            let maxV = -999999;
            let minV = 999999;
            // console.log(timeGap);
            for (let i in timeGap) {
                // console.log(i, timeGap[i])
                for (let j in timeGap[i]) {
                    // console.log(timeGap[i][j]);
                    let vSumData = sum(timeGap[i][j], d => parseFloat(d[Val_name]));

                    let xMax = max(timeGap[i][j], d => parseFloat(d[F1_name]));
                    let xMin = min(timeGap[i][j], d => parseFloat(d[F1_name]));
                    let yMax = max(timeGap[i][j], d => parseFloat(d[F2_name]));
                    let yMin = min(timeGap[i][j], d => parseFloat(d[F2_name]));
                    minV = Math.min(minV, vSumData / timeGap[i][j].length);
                    maxV = Math.max(maxV, vSumData / timeGap[i][j].length);
                    sparkBoxData.push({
                        x: x(xMin),
                        w: x(xMax) - x(xMin),
                        y: y(yMax),
                        h: y(yMin) - y(yMax),
                        v: vSumData / timeGap[i][j].length,
                        xRange: x.range(),
                        yRange: y.range(),
                        xDomain: x.domain(),
                        yDomain: y.domain()
                    })
                }
            }
            if (F1_name == 'wnd_spd' && F2_name == 'wnd_spd') {
                console.log(sparkBoxData);
            }
            let v = scaleLinear()
                .domain([minV, maxV])
                .range([0.3, 1]);
            let vScale = scaleLinear()
                .domain([minV, maxV])
                .range([0.3, 1]);
            this.valueRange = [minV.toFixed(2), maxV.toFixed(2)]


            for (let i in sparkBoxData) {
                sparkBoxData[i].fill = v(sparkBoxData[i].v);
                sparkBoxData[i].fillColor = interpolateYlGnBu(vScale(sparkBoxData[i].v));
            }
            return sparkBoxData;
        },
        mainData (data, file_name, val_name) {
            let F_sparkBoxData = []
            let margin = { top: 2, left: 40, right: 5, bottom: 20 }
            // if (dataStore.dataSelect == 'sunspots') {
            // console.log(rolling13, weight13, SN_raw_data);
            // console.log(file_name, data)
            for (let i = 0; i < file_name.length; ++i) {
                for (let j = 0; j < i + 1; ++j) {
                    // console.log(this.S_name[i], this.S_name[j]);
                    // console.log(i, j)
                    F_sparkBoxData.push({
                        x: j,
                        y: i,
                        tx: (this.elWidth - margin.left - margin.right) / file_name.length * j,
                        rx: margin.left,
                        w: (this.elWidth - margin.left - margin.right) / file_name.length,
                        ty: (this.elHeight - margin.bottom - margin.top) / file_name.length * i,
                        ry: margin.top,
                        h: (this.elHeight - margin.bottom - margin.top) / file_name.length,
                        boxData: this.calcDisSparkBox(data, (this.elHeight - margin.bottom - margin.top) / file_name.length, (this.elWidth - margin.left - margin.right) / file_name.length, 8, file_name[i], file_name[j], val_name),
                        nameX: this.nameMap[this.dataSelect][file_name[j]],
                        nameY: this.nameMap[this.dataSelect][file_name[i]],
                        nameXr: file_name[j],
                        nameYr: file_name[i]
                    })
                }
            }
            // this.show_name = this.SS_name;
            let show_name = [];
            for (let i in file_name) {
                show_name.push(file_name[i]);
            }
            // this.dataName = 'Sunspot number'
            let dateName = 'Sunspot number';
            if (this.dataSelect != 'sunspots') {
                dateName = 'PM 2.5'
            }
            // console.log(show_name)
            // console.log(F_sparkBoxData, show_name, dateName)
            return [F_sparkBoxData, show_name, dateName];
        }
    },
    created () { },
    mounted () {
        this.elHeight = this.$refs.DistributionView.offsetHeight;
        this.elWidth = this.$refs.DistributionView.offsetWidth;
        // [this.sparkBoxData, this.linePath] = this.calcSparkBox(SN_raw_data, this.elHeight, this.elWidth);
        // const dataStore = useDataStore();
        //     let margin = { top: 15, left: 50, right: 5, bottom: 30 }

        // dataStore.$subscribe((mutations, state) => {
        // console.log(222);
        // let F_sparkBoxData = []
        // } else if (dataStore.dataSelect == 'pm') {
        // for (let i = 0; i < this.F_name.length; ++i) {
        //     for (let j = 0; j < i + 1; ++j) {
        //         F_sparkBoxData.push({
        //             x: j,
        //             y: i,
        //             tx: (this.elWidth - margin.left - margin.right) / this.F_name.length * j,
        //             rx: margin.left,
        //             w: (this.elWidth - margin.left - margin.right) / this.F_name.length,
        //             ty: (this.elHeight - margin.bottom - margin.top) / this.F_name.length * i,
        //             ry: margin.top,
        //             h: (this.elHeight - margin.bottom - margin.top) / this.F_name.length,
        //             boxData: this.calcDisSparkBox(multi_data, (this.elHeight - margin.bottom - margin.top) / this.F_name.length, (this.elWidth - margin.left - margin.right) / this.F_name.length, 8, this.F_name[i], this.F_name[j], 'pm25')
        //         })
        //     }
        // }
        // this.show_name = this.F_name;
        // this.F_sparkBoxData = F_sparkBoxData;
        // this.dataName = 'PM 2.5'
        // }
        const dataStore = useDataStore();
        dataStore.$subscribe((mutations, state) => {
            console.log(mutations)
            if (mutations.events.key == 'dataSelect') {

                if (dataStore.dataSelect == 'sunspots') {

                    this.dataSelect = 'sunspots';
                    this.smoothSelect = dataStore.smooth;
                    // console.log(this.smoothSelect)
                    let s_name_select = [];
                    for (let i in this.S_name) {
                        if (this.smoothSelect[this.SS_name[i]] == 1)
                        s_name_select.push(this.S_name[i]);
                    }
                    [this.F_sparkBoxData, this.show_name, this.dataName] = this.mainData(uni_data, s_name_select, 'raw');
                } else {

                    this.dataSelect = 'pm';
                    [this.F_sparkBoxData, this.show_name, this.dataName] = this.mainData(multi_data, this.F_name, 'pm25');
                }
            }
        })
        // this.dataSelect = 'sunspots';
        // [this.F_sparkBoxData, this.show_name, this.dataName] = this.mainData(uni_data, this.S_name, 'raw');
        // console.log(this.F_sparkBoxData, this.show_name, this.dataName)
        // })


        // console.log(SN_raw_data);




        // console.log(F_sparkBoxData);
    },
}
</script>

<style scoped>
</style>
