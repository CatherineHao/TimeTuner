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

            <svg id="distributionSVG" height="100%" width="100%">
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
// import multi_data from "../assets/allData/multivariate_data/used_all_multi_data.csv";
// import multi_data from "../assets";
import multi_data from "../assets/allData/multivariate_data/smooth_data/all_smooth_multi15.csv";
import { interpolateYlGnBu } from "d3-scale-chromatic";
import { useDataStore } from "../stores/counter";
export default {
    name: 'UnitView',
    props: [],
    data () {
        return {
            elHeight: 0,
            elWidth: 0,
            F_sparkBoxData: [],
            F_name: ['raw_pm25', 'raw_temp', 'raw_rh', 'raw_psfc', 'raw_wnd_dir', 'raw_wnd_spd'],
            S_name: ['raw', 'rolling3', 'rolling6', 'rolling13', 'weighted3', 'weighted6', 'weighted13'],

            SS_name: ['RAW', 'MA-3', 'MA-6', 'MA-13', 'WMA-3', 'WMA-6', 'WMA-13'],
            show_name: [],
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
        calcDisSparkBox (data, height, width, box_num, F1_name, F2_name, Val_name) {
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
                let tx = Math.floor((data[i][F1_name] - x.domain()[0]) / timeG);
                if (tx == box_num) tx--;
                let ty = Math.floor((data[i][F2_name] - y.domain()[0]) / valG);
                if (ty == box_num) ty--;
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
            for (let i in timeGap) {
                for (let j in timeGap[i]) {
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
            for (let i = 0; i < file_name.length; ++i) {
                for (let j = 0; j < i + 1; ++j) {
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
            let show_name = [];
            for (let i in file_name) {
                show_name.push(file_name[i]);
            }
            let dateName = 'Sunspot number';
            if (this.dataSelect != 'sunspots') {
                dateName = 'PM 2.5'
            }
            return [F_sparkBoxData, show_name, dateName];
        }
    },
    created () { },
    mounted () {
        this.elHeight = this.$refs.DistributionView.offsetHeight;
        this.elWidth = this.$refs.DistributionView.offsetWidth;
        const dataStore = useDataStore();
        dataStore.$subscribe((mutations, state) => {
            console.log(mutations)
            if (mutations.events.key == 'dataSelect') {

                if (dataStore.dataSelect == 'sunspots') {

                    this.dataSelect = 'sunspots';
                    this.smoothSelect = dataStore.smooth;
                    let s_name_select = [];
                    for (let i in this.S_name) {
                        if (this.smoothSelect[this.SS_name[i]] == 1)
                        s_name_select.push(this.S_name[i]);
                    }
                    [this.F_sparkBoxData, this.show_name, this.dataName] = this.mainData(uni_data, s_name_select, 'raw');
                } else {

                    this.dataSelect = 'pm';
                    [this.F_sparkBoxData, this.show_name, this.dataName] = this.mainData(multi_data, this.F_name, 'raw_pm25');
                }
            }
        })
    },
}
</script>

<style scoped>
</style>