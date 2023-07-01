<!--
 * @Description: Profile View
 * @Author: Qing Shi
 * @Date: 2023-01-10 21:20:01
 * @LastEditTime: 2023-06-29 10:19:04
-->
<template>
    <div class="frameworkTitle">
        <div class="title">Profile View</div>
        <p class="titleTriangle"></p>

        <div style="float: right; margin-top: 3px; padding-right: 10px;">

            <el-button style="height: 30px;" @click="run()" v-loading.fullscreen.lock="fullscreenLoading">
                <svg t="1686890641424" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"
                    p-id="1477" width="20" height="20">
                    <path
                        d="M264.3 141.6l275.4 179.3 284 184.8c1 0.6 3.6 2.4 3.6 6.7 0 4.3-2.6 6.1-3.6 6.7L539.8 704 264.3 883.3c-0.2-1-0.3-2.1-0.3-3.5V145.1c0-1.3 0.2-2.5 0.3-3.5M262 66.2c-36.5 0-70 32.9-70 78.9v734.6c0 46 33.5 78.9 70 78.9 11.6 0 23.6-3.3 34.8-10.7L579 764.2l284-184.8c48.5-31.6 48.5-102.5 0-134.1L579 260.5 296.9 76.9c-11.3-7.3-23.2-10.7-34.9-10.7z"
                        fill="#606266" p-id="1478"></path>
                </svg>
            </el-button>
        </div>
    </div>
    <div class="frameworkBody">
        <div ref="ControlPanel"
            style="height: calc(45% - 10px); width: calc(100%); float: left; border: 0px solid blue; font-size: 16px; font-weight: 600; z-index: 5;">
            <div style="height: calc(12.5% -  3px);">
                <span style="float: left; font-weight: 600; margin-top: 0px;">
                    DataSet:
                </span>
                <span style="width: calc(65% - 3px); float: right;" class="dataSetClass">
                    <el-upload style="transform: translate(44%, -5px); height: 30px;"
                        class="upload-demo" action="" :http-request="uploadFile" accept=".csv">
                        <el-button style="height: 30px;">
                            <svg t="1687343622106" class="icon" viewBox="0 0 1024 1024" version="1.1"
                                xmlns="http://www.w3.org/2000/svg" p-id="2390" width="20" height="20">
                                <path
                                    d="M512 832c-176.448 0-320-143.552-320-320S335.552 192 512 192s320 143.552 320 320-143.552 320-320 320m0-704C300.256 128 128 300.256 128 512s172.256 384 384 384 384-172.256 384-384S723.744 128 512 128"
                                    fill="#3E3A39" p-id="2391"></path>
                                <path
                                    d="M683.936 470.944H544v-139.968a32 32 0 1 0-64 0v139.968h-139.936a32 32 0 0 0 0 64H480v139.968a32 32 0 0 0 64 0v-139.968h139.968a32 32 0 0 0 0-64"
                                    fill="#3E3A39" p-id="2392"></path>
                            </svg>
                        </el-button>

                    </el-upload>
                </span>
            </div>
            <div style="height: calc(12.5% -  3px); margin-top: 0px;">
                <span style="float: left; font-weight: 600; margin-top: 0px;">
                    <svg height="30" width="30" style="position: absolute;top: -2px;">
                        <path d="M10 14 L20 14" fill="none" stroke="black"></path>
                        <path d="M10 0 L 10 30" fill="none" stroke="black"></path>
                    </svg>&nbsp;&nbsp;
                    &nbsp;&nbsp;&nbsp;Variable Num:
                </span>
                <span v-if="fileValue != ''"
                    style="width: 60%; float: right; margin-top: 2px; text-align: end; margin-right: 10px;">
                    {{ profileData.variable_num }}
                </span>
            </div>
            <div style="height: calc(12.5% -  3px); margin-top: 0px;">
                <span style="float: left; font-weight: 600; margin-top: 0px;">
                    <svg height="30" width="30" style="position: absolute;top: -3px;">
                        <path d="M10 15 L20 15" fill="none" stroke="black"></path>
                        <path d="M10 0 L 10 30" fill="none" stroke="black"></path>
                    </svg>&nbsp;&nbsp;
                    &nbsp;&nbsp;&nbsp;Stationary:
                </span>
                <span v-if="fileValue != ''"
                    style="width: 60%; float: right; margin-top: 2px; text-align: end; margin-right: 10px;">
                    {{ profileData.stationary }}
                </span>
            </div>
            <div style="height: calc(12.5% -  3px); margin-top: 0px;">
                <span style="float: left; font-weight: 600; margin-top: 0px;">
                    <svg height="30" width="30" style="position: absolute; top: -4px;">
                        <path d="M10 0 L 10 16" fill="none" stroke="black"></path>
                        <path d="M10 16 L20 16" fill="none" stroke="black"></path>
                    </svg>&nbsp;&nbsp;
                    &nbsp;&nbsp;&nbsp;Periodicity:

                </span>
                <span v-if="fileValue != ''"
                    style="width: 60%; float: right; margin-top: 2px; text-align: end; margin-right: 10px;">
                    {{ profileData.periodicity }}
                </span>
            </div>
            <hr>
            <div style="height: calc(12.5% -  3px); margin-top: 5px; margin-bottom: 5px;">
                <span style="float: left; font-weight: 600; margin-top: 0px;">
                    Model:
                </span>
                <span style="width: calc(65% - 3px); float: right;" class="dataSetClass">
                    <el-select v-model="modelValue" class="m-2" placeholder="Please select" size="large"
                        style="width: 100%;font-weight: 600; text-align: center;">
                        <el-option v-for="item in modelOptions" :key="item.value" :label="item.label" :value="item.value"
                            style="text-align: center;" />
                    </el-select>
                </span>
            </div>
            <hr>

            <div style="height: calc(12.5% -  3px); margin-top: 3px;">

                <span style="float: left; font-weight: 600; margin-top: 0px;">
                    Transformation:

                </span>
                <span style="width: calc(65% - 3px); float: right;" class="dataSetClass">
                    <el-select v-model="methodSelect" class="m-2" placeholder="Please select" size="large"
                        style="font-weight: 600; width: 100%" multiple collapse-tags collapse-tags-tooltip
                        :max-collapse-tags="2">

                        <el-option style="text-align: center;" v-for="item in methodOptions" :key="item.label" :label="item.label" :disabled="item.status == 0"
                            :value="item.label" />
                    </el-select>
                </span>
            </div>
            <div v-show="smoothTag == 1" style="height: calc(12.5% -  3px); margin-top: 3px;">

                <span style="float: left; font-weight: 600; margin-top: 0px;">
                    <svg height="34" width="30" style="position: absolute; top: -4px;">
                        <path d="M10 0 L 10 16" fill="none" stroke="black"></path>
                        <path d="M10 16 L 10 34" v-if="skipTag == 1 || padTag == 1 || reshapeTag == 1" fill="none" stroke="black"></path>
                        <path d="M10 16 L20 16" fill="none" stroke="black"></path>
                    </svg>&nbsp;&nbsp;
                    &nbsp;&nbsp;&nbsp;Smoothing:

                </span>
                <span style="width: calc(65% - 3px); float: right;" class="dataSetClass">
                    <el-select v-model="smoothValue" class="m-2" placeholder="Please select" size="large"
                        style="font-weight: 600; width: 100%" multiple collapse-tags collapse-tags-tooltip
                        :max-collapse-tags="2">

                        <el-option-group v-for="group in smoothOptions" :key="group.label" :label="group.label">
                            <el-option style="text-align: center;" v-for="item in group.options" :key="item.value"
                                :label="item.label" :value="item.value" />
                        </el-option-group>
                    </el-select>
                </span>
            </div>
            <div v-show="skipTag == 1" style="height: calc(12.5% -  3px); margin-top: 3px;">

                <span style="float: left; font-weight: 600; margin-top: 0px;">
                    <svg height="34" width="30" style="position: absolute; top: -8px;">
                        <path d="M10 0 L 10 20" fill="none" stroke="black"></path>
                        <path d="M10 20 L20 20" fill="none" stroke="black"></path>
                        <path d="M10 16 L 10 34" v-if="padTag == 1 || reshapeTag == 1" fill="none" stroke="black"></path>
                    </svg>&nbsp;&nbsp;
                    &nbsp;&nbsp;&nbsp;Sampling:

                </span>
                <span style="width: calc(65% - 3px); float: right;" class="dataSetClass">
                    <el-select v-model="skipValue" class="m-2" placeholder="Please select" size="large"
                        style="font-weight: 600; width: 100%" multiple collapse-tags collapse-tags-tooltip
                        :max-collapse-tags="3" popper-class="skipClass">
                        <el-option v-for="item in skipOptions" :key="item" :label="item" :value="item"
                            style="text-align: center;" />
                    </el-select>
                </span>
            </div>
            <div v-show="padTag == 1" style="height: calc(12.5% -  3px); margin-top: 3px;">

                <span style="float: left; font-weight: 600; margin-top: 0px;">
                    <svg height="34" width="30" style="position: absolute; top: -8px;">
                        <path d="M10 0 L 10 20" fill="none" stroke="black"></path>
                        <path d="M10 20 L20 20" fill="none" stroke="black"></path>
                        <path d="M10 16 L 10 34" v-if="reshapeTag == 1" fill="none" stroke="black"></path>
                    </svg>&nbsp;&nbsp;
                    &nbsp;&nbsp;&nbsp;Padding:

                </span>
                <span style="width: calc(65% - 3px); float: right;" class="dataSetClass">
                    <el-select v-model="padValue" class="m-2" placeholder="Please select" size="large"
                        style="font-weight: 600; width: 100%" collapse-tags collapse-tags-tooltip :max-collapse-tags="3">
                        <el-option v-for="item in padOptions" :key="item.value" :label="item.label" :value="item.value"
                            style="text-align: center;" :disabled="item.dis" />
                    </el-select>
                </span>
            </div>
            <div v-show="reshapeTag == 1" style="height: calc(12.5% -  3px); margin-top: 3px;">

                <span style="float: left; font-weight: 600; margin-top: 0px;">
                    <svg height="30" width="30" style="position: absolute; top: -8px;">
                        <path d="M10 0 L 10 20" fill="none" stroke="black"></path>
                        <path d="M10 20 L20 20" fill="none" stroke="black"></path>
                    </svg>&nbsp;&nbsp;
                    &nbsp;&nbsp;&nbsp;Reshaping:

                </span>
                <span style="width: calc(65% - 3px); float: right;" class="dataSetClass">
                    <el-select v-model="reshapeValue" class="m-2" placeholder="Please select" size="large"
                        style="font-weight: 600; width: 100%" collapse-tags collapse-tags-tooltip :max-collapse-tags="3">
                        <el-option v-for="item in reshapeOptions" :key="item.value" :label="item.label" :value="item.value"
                            style="text-align: center;" />
                    </el-select>
                </span>
            </div>
        </div>
        <div ref="resTable"
            style="height: calc(55% + 10px); width: calc(100%); float: right; overflow:auto; font-size: 18px; margin-top: 5px;">
            <el-table v-show="tableTag == 1" :data="tableData" style="width: calc(100% - 0px)" height="100%"
                :header-cell-style="{ 'font-size': '16px', 'background-color': 'rgb(235, 235, 235)', 'height': '40px', 'text-algin': 'left', 'font-weight': '600' }"
                :cell-style="{ 'font-size': '14px', 'height': '15px' }" :row-class-name="selectRowStyle" border
                @row-click="rowClick">
                <el-table-column prop="smooth" label="Smooth" width="82" />
                <el-table-column prop="skip" label="Skip" width="62" />
                <el-table-column label="Train" :width="(elWidth - 142) / 3" sortable :sort-by="'train'">
                    <template #default="scope">
                        <svg width="100%" height="18">
                            <rect :x="0" :y="3" :width="scope.row.train_bar.w" :height="15" :fill="'orange'"
                                :fill-opacity="1" :stroke="'rgba(200, 200, 200, 0)'"> </rect>
                            <text x="2" y="15" font-size="12">{{ scope.row.train_bar.v }}</text>
                        </svg>
                    </template>
                </el-table-column>

                <el-table-column label="Val." :width="(elWidth - 142) / 3" sortable :sort-by="'test'">
                    <template #default="scope">
                        <svg width="100%" height="18">
                            <rect :x="0" :y="3" :width="scope.row.test_bar.w" :height="15" :fill="'orange'"
                                :stroke="'rgba(200, 200, 200, 0)'" :fill-opacity="1"></rect>
                            <text x="2" y="15" font-size="12">{{ scope.row.test_bar.v }}</text>
                        </svg>
                    </template>
                </el-table-column>

                <el-table-column label="ACF" :width="(elWidth - 142) / 3" sortable :sort-by="'acf'">
                    <template #default="scope">
                        <svg width="100%" height="18">
                            <rect :x="0" :y="3" :width="scope.row.acf_bar.w" :height="15" :fill="'orange'"
                                :stroke="'rgba(200, 200, 200, 0)'" :fill-opacity="1"></rect>
                            <text x="2" y="15" font-size="12">{{ scope.row.acf_bar.v }}</text>
                        </svg>
                    </template>
                </el-table-column>
            </el-table>
        </div>
    </div>
</template>

<script>
import { scaleLinear } from 'd3-scale';
import { select, selectAll } from 'd3-selection';
import { useDataStore } from "../stores/counter";
import { ElLoading } from 'element-plus'
export default {
    name: 'PV',
    props: [],
    data () {
        return {
            elHeight: 0,
            elWidth: 0,
            smoothTag: 0,
            skipTag: 0,
            padTag: 0,
            reshapeTag: 0,
            tableTag: 0,
            fullscreenLoading: false,
            methodOptions: [{label: "Smoothing", status: 1}, {label: "Sampling", status: 1}, {label: "Padding", status: 1}, {label: "Reshaping", status: 1}],
            methodSelect: [],
            smoothSelect: {},
            skipSelect: {},
            smoothValue: [],
            skipValue: [],
            padValue: '',
            reshapeValue: '',
            normalizeValue: '',
            padOptions: [],
            reshapeOptions: [],
            skipOptions: [],
            smoothOptions: {},
            periodInput: '',
            fileValue: '',
            tableData: [],
            modelValue: null,
            modelOptions: [{
                value: 'Long Short Term Memory',
                label: 'Long Short Term Memory',
            }],
            tableData: [],
            selectRowClass: '',
            file_name: ''
        }
    },
    methods: {
        uploadFile (param) {
            let fileObj = param.file
            let form = new FormData()
            form.append("fileToUpload", fileObj)
            const dataStore = useDataStore();
            this.file_name = form.get("fileToUpload").name
            dataStore.uploadData({
                filename: form.get("fileToUpload").name
            });
        },
        run () {
            const loading = ElLoading.service({
                lock: true,
                text: 'Please waiting...',
                background: 'rgba(0, 0, 0, 1)',
            })
            setTimeout(() => {
                loading.close()
                let skip = {};
                let smooth = {};
                for (let i in this.smoothValue) {
                    smooth[this.smoothValue[i]] = 1;
                }
                for (let i in this.skipValue) {
                    skip[this.skipValue[i]] = 1;
                }
                this.smoothSelect = smooth;
                this.skipSelect = skip;

                const dataStore = useDataStore();
                dataStore.smooth = smooth;
                dataStore.skip = skip;
                dataStore.fetchAllData({
                    filename: this.file_name
                });
            },  1000)
        },
        cellClassName ({ row, column, rowIndex, columnIndex }) {
            if (columnIndex == 0) {
                return { 'padding': '0px' }
            }
        },
        selectRowStyle (data) {
            if (data.row.class_name == this.selectRowClass)
                return 'warning-row';
            return '';
        },
        rowClick (row, event, column) {
            let tdata = [];
            let class_name = (row['dataset_name'] == 'rawdata' ? 'raw' : row['dataset_name']) + '_' + row['skip']
            this.selectRowClass = class_name;
            console.log(this.selectRowClass)
            console.log(class_name);
            selectAll('.corr_cir').attr('opacity', (d, i) => {
                if (d.class_name == class_name) {
                    tdata.push(d);
                }
                return d.isShow ? 0 : 0.5;
            }).attr('fill', '#d9d9d9')
            const dataStore = useDataStore();
            dataStore.selectRowClass = class_name;
            selectAll('.' + 'black_select_row').attr('stroke-width', 0)
            select('#' + class_name).attr('stroke-width', 3)
            
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
                .attr('r', 3)
                .attr('stroke', 'black')
                .attr('stroke-width', 0.5)
                .attr('fill', d => d.fill)
                .attr('cursor', 'pointer')
                .on('click', (e, d) => {
                    console.log(d)
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
        formatNum (num) {
            let v = Math.round(parseFloat(num) * 100) / 100;
            let arrayNum = v.toString().split(".");
            if (arrayNum.length == 1) {
                return v.toString() + ".00";
            }
            if (arrayNum.length > 1) {
                if (arrayNum[1].length < 2) {
                    return v.toString() + "0";
                }
                return v;
            }
        },
        translate (x, y, deg) {
            return `translate(${x}, ${y}) rotate(${deg})`;
        },
        calcTable (data) {
            let tmpData = [];
            let max_train = 0,
                max_test = 0,
                max_acf = 0
            let file_cnt = 0;
            for (let i in data) {
                for (const j in data[i].predic_info) {
                    let d = data[i].predic_info[j];
                    let tmp = new Object();
                    tmp['dataset_name'] = data[i].dataset_name;

                    file_cnt++;
                    let smooth_name = '';
                    let raw_smooth_name = '';
                    if (data[i].dataset_name[1] == 'a') {
                        smooth_name = 'RAW';
                        raw_smooth_name = 'raw';
                    } else {
                        if (data[i].dataset_name[1] == 'o') {
                            smooth_name = 'MA-';
                            raw_smooth_name = 'rolling';
                        } else if (data[i].dataset_name[1] == 'e') {
                            smooth_name = 'WMA-';
                            raw_smooth_name = 'weighted';
                        }
                        // console.log(typeof(data[i].dataset_name));
                        let stcnt = data[i].dataset_name;
                        let cnt = stcnt.substring(stcnt.length - 2);
                        if (!isNaN(Number(cnt))) {
                            smooth_name = smooth_name + cnt;
                            raw_smooth_name = raw_smooth_name + cnt;
                        } else {
                            smooth_name = smooth_name + cnt[1];
                            raw_smooth_name = raw_smooth_name + cnt[1];
                        }
                    }
                    if (this.smoothSelect[smooth_name] != 1 || this.skipSelect[parseInt(d.skip)] != 1) {
                        continue;
                    }
                    tmp['smooth'] = smooth_name;
                    tmp['skip'] = d.skip;
                    tmp['train'] = (d['train_MSE']);
                    tmp['test'] = (d['val_MSE']);
                    tmp['acf'] = (d['ACF']);
                    tmp['class_name'] = data[i].dataset_name + '_' + d['skip'];
                    max_acf = Math.max(max_acf, parseFloat(data[i].predic_info[j]['ACF']));
                    max_train = Math.max(max_train, parseFloat(data[i].predic_info[j]['train_MSE']));
                    max_test = Math.max(max_test, parseFloat(data[i].predic_info[j]['val_MSE']));
                    tmpData.push(tmp);
                }
            }
            let leftT = 160;
            let barS = this.elWidth - leftT;
            let trainScale = scaleLinear([0, max_train], [0, ((barS) / 3) * 0.9]);
            let testScale = scaleLinear([0, max_test], [0, ((barS) / 3) * 0.9]);
            let acfScale = scaleLinear([0, max_acf], [0, ((barS) / 3) * 0.9]);
            for (let i in tmpData) {
                tmpData[i]['train_bar'] = {
                    x: 0,
                    w: trainScale(tmpData[i]['train']),
                    v: (tmpData[i]['train'].toFixed(4)).toString().slice(1)
                };
                tmpData[i]['test_bar'] = {
                    x: barS / 3,
                    w: testScale(tmpData[i]['test']),
                    v: (tmpData[i]['test'].toFixed(4)).toString().slice(1)
                };
                tmpData[i]['acf_bar'] = {
                    x: barS * 2 / 3,
                    w: acfScale(tmpData[i]['acf']),
                    v: (tmpData[i]['acf'].toFixed(4)).toString().slice(1)
                };
            }
            return tmpData;
        }
    },
    watch: {
        methodSelect () {
            for (let i in this.methodSelect) {
                if (this.methodSelect[i] == 'Smoothing') {
                    this.smoothTag = 1;
                }
                if (this.methodSelect[i] == "Sampling") {
                    this.skipTag = 1;
                }

                if (this.methodSelect[i] == 'Padding') {
                    this.padTag = 1;
                }
                if (this.methodSelect[i] == "Reshaping") {
                    this.reshapeTag = 1;
                }
            }
        }
    },
    created () { },
    mounted () {
        this.elHeight = this.$refs.ControlPanel.offsetHeight;
        this.elWidth = this.$refs.ControlPanel.offsetWidth;
        const dataStore = useDataStore()
        dataStore.$subscribe((mutations, state) => {
            // console.log(mutations)
            if (mutations.events.key == 'system_data') {
                this.tableTag = 1;
                this.tableData = this.calcTable(dataStore.system_data.model_result);
            }
            if (mutations.events.key == 'selectRowClass') {
                this.selectRowClass = dataStore.selectRowClass;
            }
            if (mutations.events.key == 'profileData') {
                this.profileData = dataStore.profileData;
                this.smoothOptions = this.profileData.smooth;
                this.skipOptions = this.profileData.sample;
                this.padOptions = this.profileData.pad;
                if (this.profileData.padTag == -1)
                    this.methodOptions[2].status = 0;
                this.reshapeOptions = this.profileData.reshape;
                if (this.profileData.reshapeTag == -1)
                    this.methodOptions[3].status = 0;
                this.fileValue = this.profileData.file_name;
            }
        })
    },
}
</script>

<style>
.el-loading-spinner {
    font-size: 80px;
    font-weight: normal;
}

.el-loading-mask .el-loading-spinner .el-loading-text {
    font-size: 25px;
}

.el-upload-list {
    margin-top: 0px;
    width: 180px;
    transform: translate(-100px, -30px);
}

.dataSetClass .el-input__inner {
    font-weight: 600;
    text-align: center;
    border: 0px;
}

.el-button {
    padding: 0px;
    padding-top: 2px;
}

.el-input__wrapper {
    height: 30px;
}

.el-table .warning-row {
    background-color: #ebebeb;
}

.el-table .cell {
    text-align: left;
}</style>
