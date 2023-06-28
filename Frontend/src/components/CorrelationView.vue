<!--
 * @Description: 
 * @Author: Qing Shi
 * @Date: 2023-01-10 21:20:01
 * @LastEditTime: 2023-01-12 02:11:55
-->
<template>
    <div class="frameworkTitle">
        <div class="title">Correlation View</div>
        <p class="titleTriangle"></p>
        <!-- <svg height="30px" width="200px" style="float: right;">
            <rect v-for="(t, i) in legendRect" :key="'lr' + i" :x="20 + i * (150 / legendRect.length)" y="10" height="15"
                :width="(150 / legendRect.length)" :fill="t" :stroke="t"></rect>
        </svg> -->
    </div>
    <div class="frameworkBody">
        <div ref="CorrelationView" style="height: 100%; width: 100%;">
            <!-- <svg id="CorrelationView" height="100%" width="100%">
                        <text v-for="(item, i) in smooth" x="10" :y="i * (elHeight) / 3 + 50" font-size="20">{{ item }}</text>
                        <text v-for="(item, i) in sample" :x="110 + i * (elWidth - 80) / 3 + (i == 1 ? 38 : i == 2 ? 25 : 0)" :y="15" font-size="20">{{ item }}</text>
                        <g v-for="(item, ii) in mData">
                            <rect v-for="(item1, i) in item[0]" :transform="translate(0, ii * (elHeight) / 3, 0)" :x="75 + (i % 8) * 18" :y="25 + 18 * (parseInt(i / 8))" :width="18" :height="18" :fill="item1" stroke="rgba(229, 229, 229)"></rect>
                            
                            <rect v-for="(item2, i) in item[1]" :transform="translate(180, ii * (elHeight) / 3, 0)" :x="75 + (i) * 18" :y="34" :width="18" :height="18" :fill="item2" stroke="rgba(229, 229, 229)"></rect>

                            
                            <rect v-for="(item2, i) in item[2]" :transform="translate(342, ii * (elHeight) / 3, 0)" :x="75 + (i) * 18" :y="34" :width="18" :height="18" :fill="item2" stroke="rgba(229, 229, 229)"></rect>
                        </g>
                    </svg> -->

            <svg id="CorrelationView" height="100%" width="100%">
                <text v-for="(item, i) in smooth" :key="'sm' + i" x="0" y="0"
                    :transform="translate(55 + i * (elWidth - 60) / (27 / 2) + (elWidth - 60) / (27), 20, -10)" text-anchor="middle">{{ item }}</text>
                <text v-for="(item, i) in sample" :key="'sa' + i" x="0"
                    :y="i * (elHeight - 30) / 4 + 30 + (elHeight - 30) / 8" font-size="16">{{ item }}</text>
                <g :transform="translate(55, 30, 0)">
                    <rect v-for="(item, i) in heatData" :key="'sr' + i" :x="item.x1" :y="item.y" :width="item.w1"
                        :height="item.h" :fill="item.c1" stroke="white" stroke-width="3"></rect>
                    <rect v-for="(item, i) in heatData" :key="'sr' + i" :x="item.x2" :y="item.y" :width="item.w2"
                        :height="item.h" :fill="item.c2" stroke="white" stroke-width="3"></rect>
                    <rect v-for="(o, i) in 36" :key="'st' + i" :x="(i % 9) * (elWidth - 60) / (27 / 2)" :y="Math.floor(i / 9) * (elHeight - 30) / 4" :width="(elWidth - 60) / (27 / 2)" :height="(elHeight - 30) / 4" fill="none" stroke="white"></rect>
                </g>
                <g id="cor_legend_g" :transform="translate(elWidth - 190, 30, 0)"></g>
            </svg>
        </div>
    </div>
</template>
<script>
import * as vsup from 'vsup';
import res_data from '../assets/model_skip_results.json';
import { interpolateRdBu, interpolateYlOrRd, scaleLinear, select } from 'd3';
export default {
    name: 'CorrelationView',
    props: [],
    data () {
        return {
            elHeight: 100,
            elWidth: 100,
            sample: ['skip-13', 'skip-6', 'skip-3', 'skip-1'],
            smooth: ['raw', 'rolling3', 'rolling6', 'rolling9', 'rolling13', 'weighted3', 'weighted6', 'weighted9', 'weighted13'],
            legendRect: [],
            mData: [],
            heatData: []
        }
    },
    methods: {
        translate (x, y, deg) {
            return `translate(${x}, ${y}) rotate(${deg})`;
        },
        legend () {
            let colors = interpolateRdBu;
            let legendL = [];
            for (let i = 0; i <= 100; ++i) {
                legendL.push(colors(i / 100));
            }
            return legendL;
        },
        calcMatrix () {
            let colors = interpolateRdBu;
            let mData = [];
            for (let i = 1; i <= 3; ++i) {
                let td1 = [], td2 = [], td3 = [];
                for (let j = 0; j < 16; ++j) {
                    td1.push(colors(Math.random()));
                }
                for (let j = 0; j < 7; ++j) {
                    td2.push(colors(Math.random()));
                }
                for (let j = 0; j < 3; ++j) {
                    td3.push(colors(Math.random()));
                }
                mData.push([td1, td2, td3]);
            }
            return mData;
        },
        calcData (data) {
            console.log(data);
            let tmpData = new Array();
            let max_vloss = -99999;
            let min_vloss = 99999;
            let max_loss = -99999;
            let min_loss = 99999;
            let min_acf = 999999;
            let max_acf = -999999;
            let min_lo = 999999;
            let max_lo = -999999;
            for (let i = 0; i < 9; ++i) {
                for (const j in data[i].predic_info) {
                    let d = data[i].predic_info[j];
                    let tmp = new Object();
                    tmp['dataset_name'] = data[i].dataset_name;
                    tmp['skip'] = d.skip;
                    // console.log(d.skip);
                    tmp['train'] = d['loss=mean_squared_error'];
                    tmp['test'] = d['val_loss=val_mse'];
                    tmp['acf'] = d['ACF'];
                    max_loss = Math.max(max_loss, tmp['train']);
                    min_loss = Math.min(min_loss, tmp['train']);
                    max_vloss = Math.max(max_vloss, tmp['test']);
                    min_vloss = Math.min(min_vloss, tmp['test']);
                    min_lo = Math.min(min_lo, tmp['train'], tmp['test']);
                    max_lo = Math.max(max_lo, tmp['train'], tmp['test']);
                    min_acf = Math.min(min_acf, tmp['acf']);
                    max_acf = Math.max(max_acf, tmp['acf']);
                    tmp['x1'] = i * (this.elWidth - 60) / (27 / 2);
                    tmp['w1'] = 6 * (this.elWidth - 60) / (27 * 7 / 2);
                    tmp['x2'] = i * (this.elWidth - 60) /(27 / 2) + tmp['w1'];
                    tmp['w2'] = (this.elWidth - 60) / (27 * 7 / 2);
                    tmp['y'] = j * (this.elHeight - 30) / 4;
                    tmp['h'] = (this.elHeight - 30) / 4;
                    tmpData.push(tmp);
                }
            }
            let c1Scale = scaleLinear([min_loss, max_loss], [0, 1]);
            let c2Scale = scaleLinear([min_vloss, max_vloss], [0, 1]);

            
            let heatColor = interpolateYlOrRd;
            // let heatColor = interpolateRdBu;
            let quantization = vsup.quantization().branching(2).layers(4).valueDomain([min_acf, max_acf]).uncertaintyDomain([max_lo, min_lo]);
            let heatScale = vsup.scale().quantize(quantization).range(heatColor);

            var legend = vsup.legend.arcmapLegend();

            legend
                .scale(heatScale)
                .size(150)
                .x(0)
                .y(0)
                .vtitle("ACF")
                .utitle("RMSE");
            select('#cor_legend_g').call(legend);
            
            for (let i in tmpData) {
                // tmpData[i]['c1'] = interpolateYlOrRd(c1Scale(tmpData[i]['train']));
                tmpData[i]['c1'] = heatColor(tmpData[i]['acf'], tmpData[i]['train']);
                // tmpData[i]['c2'] = interpolateYlOrRd(c2Scale(tmpData[i]['test']));
                tmpData[i]['c2'] = heatColor(tmpData[i]['acf'], tmpData[i]['test']);
            }
            console.log(tmpData);
            return tmpData;
        }
    },
    created () {
    },
    mounted () {
        this.elHeight = this.$refs.CorrelationView.offsetHeight;
        this.elWidth = this.$refs.CorrelationView.offsetWidth;
        // this.legendRect = this.legend();
        // this.mData = this.calcMatrix();
        // console.log(this.mData)
        // console.log(this.elHeight)
        this.heatData = this.calcData(res_data);

    },
}
</script>
<style scoped>
/* *,
*::before,
*::after {
    font-weight: normal;
} */
</style>
