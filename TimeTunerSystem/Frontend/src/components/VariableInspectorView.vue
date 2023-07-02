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
 * @Description: Variable Inspector View
 * @Author: Qing Shi
 * @Date: 2023-06-29 10:17:17
 * @LastEditors: Qing Shi
 * @LastEditTime: 2023-07-01 23:34:07
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
                            :transform="translate(37, 35 + i * (elHeight - 30) / show_name.length, -60)">{{ o }}</text>
                    </g>
                    <g>
                        <text v-for="(o, i) in show_name" :key="'F_leg' + i" :x="0" :y="0" :font-size="14"
                            :transform="translate(40 + (elWidth - 40) / show_name.length / 2 + (elWidth - 40) / show_name.length * i, (elHeight - 30) + 25, 0)"
                            font-weight="100" text-anchor="middle">{{ o }}</text>
                    </g>
                    <g v-for="(o, i) in matrixData" :key="'fsb' + i" :transform="translate(o.tx, o.ty, 0)">
                        <g :transform="translate(40, 2, 0)">
                            <rect v-for="(oo, r_i) in o.boxData" :key="'fsbr' + r_i" :x="oo.x" :y="oo.y" :width="oo.w"
                                :height="oo.h" :fill="oo.fillColor" :opacity="oo.fill" stroke="white"></rect>
                        </g>
                        <rect :x="o.rx" :y="o.ry" :width="o.w" :height="o.h" :class="'unitRect'" :id="'unit' + i"
                            fill="black" stroke="#304051" fill-opacity="0" stroke-width="0.7"
                            @mouseenter="mouseoverFeature(o.boxData, o.nameX, o.nameY, i)" @mouseout="mouseoutFeature()"
                            @click="clickFeature(o.nameX, o.nameY)"></rect>
                    </g>
                </g>
                <g>
                    <g :transform="translate(elWidth * 2 / 3 - 25, 15, 0)" id="mouseRect" :opacity="selectTag == 1 ? 1 : 0">

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
import { scaleLinear } from "d3-scale";
import { select, selectAll } from "d3-selection";
import { interpolateYlGnBu } from "d3-scale-chromatic";
import { useDataStore } from "../stores/counter";
export default {
    name: 'VIV',
    props: [],
    data () {
        return {
            elHeight: 0,
            elWidth: 0,
            matrixData: [],
            show_name: [],
            dataName: '',
            valueRange: [],
            selectRect: [],
            selectTag: 0,
            dataSelect: 'pm',
            smoothSelect: {},
        }
    },
    methods: {
        /**
         * @description: set the transformation
         * @param {float} x translate x px
         * @param {float} y translate y px
         * @param {float} deg rotate degrees
         * @return {string} the transformation string
         */
        translate (x, y, deg) {
            return `translate(${x}, ${y}) rotate(${deg})`;
        },
        /**
         * @description: mouseover a matrix block
         * @param {*} data the data of this piece
         * @param {*} nameX characteristic name of the column
         * @param {*} nameY characteristic name of the row
         * @param {*} num the index of the matrix block
         * @return {*}
         */
        mouseoverFeature (data, nameX, nameY, num) {
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
                nameY: nameY
            };
        },
        /**
         * @description: mouse out the matrix block
         * @return {*}
         */
        mouseoutFeature () {
            this.selectTag = 0;
            selectAll('.unitRect').attr('stroke-width', 1);
        },
        /**
         * @description: select (click) a matrix block
         * @param {*} nameX characteristic name of the column
         * @param {*} nameY characteristic name of the row
         * @return {*}
         */
        clickFeature (nameX, nameY) {
            const dataStore = useDataStore();
            dataStore.rowSelectTag = 1;
            dataStore.selectSmooth = [nameX, nameY];
        },
        /**
         * @description: calculate the data of the selected matrix block
         * @param {*} data all smoothed data
         * @param {*} height height of a matrix block
         * @param {*} width width of a matrix block
         * @param {*} box_num the number of divisions within the matrix block
         * @param {*} F1_name characteristic name of the row
         * @param {*} F2_name characteristic name of the column
         * @param {*} Val_name observed indicator
         * @return {*} the data of the selected matrix block
         */
        calcDisSparkBox (data, height, width, box_num, F1_name, F2_name, Val_name) {
            let margin = ({ top: 0, right: 0, bottom: 0, left: 0 });

            let y = scaleLinear()
                .domain([min(data, d => parseFloat(d[F2_name])), max(data, d => parseFloat(d[F2_name]))])
                .range([height - margin.bottom, margin.top])
            let x = scaleLinear()
                .domain([min(data, d => parseFloat(d[F1_name])), max(data, d => parseFloat(d[F1_name]))])
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
        /**
         * @description: main processing function
         * @param {*} data all smoothed data
         * @param {*} val_name observed indicator
         * @param {*} variable_num data variable number
         * @return {*} [matrix data, matrix name, legend name]
         */
        mainData (data, val_name, variable_num) {
            let matrixData = []
            let margin = { top: 2, left: 40, right: 5, bottom: 20 }
            let file_name = [];
            for (let i in data[0]) {
                if (i == 'id' || i == 'time') {
                    continue;
                }
                if (variable_num == 1 && this.smoothSelect[i] != 1)
                    continue
                file_name.push(i);
            }
            for (let i = 0; i < file_name.length; ++i) {
                for (let j = 0; j < i + 1; ++j) {
                    matrixData.push({
                        x: j,
                        y: i,
                        tx: (this.elWidth - margin.left - margin.right) / file_name.length * j,
                        rx: margin.left,
                        w: (this.elWidth - margin.left - margin.right) / file_name.length,
                        ty: (this.elHeight - margin.bottom - margin.top) / file_name.length * i,
                        ry: margin.top,
                        h: (this.elHeight - margin.bottom - margin.top) / file_name.length,
                        boxData: this.calcDisSparkBox(data, (this.elHeight - margin.bottom - margin.top) / file_name.length, (this.elWidth - margin.left - margin.right) / file_name.length, 8, file_name[i], file_name[j], val_name),
                        nameX: file_name[j],
                        nameY: file_name[i]
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
            return [matrixData, show_name, dateName];
        },
        /**
         * @description: data processing
         * @param {*} data
         * @return {*}
         */
        dataConvert (data) {
            let featureSet = [];
            for (let i in data) {
                featureSet.push(i);
            }
            console.log(data[featureSet[0]]);
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
    created () { },
    mounted () {
        this.elHeight = this.$refs.DistributionView.offsetHeight;
        this.elWidth = this.$refs.DistributionView.offsetWidth;
        const dataStore = useDataStore();

        /**
         * @description: watch the data changes in the store
         * @return {*}
         */
        dataStore.$subscribe((mutations, state) => {
            if (mutations.events.key == 'system_data') {
                this.smoothSelect = dataStore.smooth;
                this.dataSelect = dataStore.system_data.file_name;
                let variable_num = parseInt(dataStore.profileData.variable_num);
                let temporal_data = JSON.parse(dataStore.system_data.temporal_data);
                let res_data = this.dataConvert(temporal_data);
                [this.matrixData, this.show_name, this.dataName] = this.mainData(res_data, dataStore.system_data.select_attr, variable_num);
            }
        })
    },
}
</script>

<style scoped></style>
