<!--
 * @Description: Prediction Comparator View
 * @Author: Qing Shi
 * @Date: 2023-06-29 10:17:17
 * @LastEditors: Qing Shi
 * @LastEditTime: 2023-07-01 22:38:10
-->
<template>  
    <div class="frameworkTitle" style="padding-right: 10px">
        <div class="title">Prediction Comparator View</div>
        <p class="titleTriangle"></p>
        <div style="float: right; margin-top: 3px">
            <span style="margin-right: 10px">
                <span>X-Axis: </span>
                <el-select v-model="xAxisValue" class="m-2" placeholder="Select" style="width: 100px">
                    <el-option v-for="(item, i) in xAxisOption" :key="item" :label="item.label" :value="item.value" />
                </el-select>
            </span>
            <span style="margin-right: 10px">
                <span>Y-Axis: </span>
                <el-select v-model="yAxisValue" class="m-2" placeholder="Select" style="width: 100px">
                    <el-option v-for="(item, i) in yAxisOption" :key="item" :label="item.label" :value="item.value" />
                </el-select>
            </span>
            <el-button style="height: 30px; margin-right: 0px" @click="legendStatus">
                <img src="../assets/img/colorLegend.png" alt="" width="20" height="20" />
            </el-button>

            <el-button style="height: 30px" @click="refresh()">
                <svg t="1680060651492" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"
                    p-id="2903" width="20" height="20">
                    <path
                        d="M810.666667 273.706667L750.293333 213.333333 512 451.626667 273.706667 213.333333 213.333333 273.706667 451.626667 512 213.333333 750.293333 273.706667 810.666667 512 572.373333 750.293333 810.666667 810.666667 750.293333 572.373333 512z"
                        p-id="2904" fill="#606266"></path>
                </svg>
            </el-button>
        </div>
    </div>
    <div class="frameworkBody">
        <div ref="modelExplainer" :style="{
            height: '100%',
            width: elHeight + 25 + 'px',
            float: 'right',
            cursor: 'crosshair',
        }">
            <svg id="modelExplainer" height="100%" width="100%">
                <g id="scatter"></g>
                <g id="legend_g_s" :opacity="legendTag == 0 ? 0 : 1"></g>
                <g id="axis_g">
                    <g id="x_axis_g" :transform="translate(0, 0, 0)"></g>
                    <g id="y_axis_g" :transform="translate(0, 0, 0)"></g>
                </g>
            </svg>
        </div>
        <div ref="modelTable" :style="{
            height: '100%',
            width: `calc(36% - 5px)`,
            float: 'left',
            overflow: 'auto',
            'font-size': '18px',
        }">
            <el-table v-if="showTable == 1" :data="tableData" style="width: calc(100% - 0px)" height="100%"
                :header-cell-style="{
                    'font-size': '16px',
                    'background-color': 'rgb(235, 235, 235)',
                    height: '40px',
                    'text-algin': 'start',
                }" :cell-style="{ 'font-size': '14px', height: '15px' }" :row-class-name="selectRowStyle"
                @row-click="selectPredict" :row-style="{ height: '18px' }" border>
                <el-table-column label="Smooth" prop="smooth_name" width="82" />
                <el-table-column label="Skip" prop="skip" width="62" />
                <el-table-column label="RMSE" sortable :sort-by="'rmse_v'">
                    <template #default="scope">
                        <svg width="100%" height="18">
                            <rect :x="0" :y="3" :width="scope.row.d1.w < 0 ? 0 : scope.row.d1.w" :height="15"
                                :fill="'orange'" :fill-opacity="1" :stroke="'rgba(200, 200, 200, 0)'"></rect>
                            <text x="2" y="15" font-size="12">{{ scope.row.d1.v }}</text>
                        </svg>
                    </template>
                </el-table-column>
                <el-table-column :label="xAxisValue == 0 ? 'CORR.' : 'SHAP'" :prop="xAxisValue == 0 ? 'norm_corr' : 'shap'"
                    sortable>
                    <template #default="scope">
                        <svg width="100%" height="18">
                            <rect :x="scope.row[xAxisValue == 0 ? 'd2' : 'd3']['x']" :y="3" :width="scope.row[xAxisValue == 0 ? 'd2' : 'd3'].w < 0
                                ? 0
                                : scope.row[xAxisValue == 0 ? 'd2' : 'd3'].w
                                " :height="15" :fill="scope.row[xAxisValue == 0 ? 'd2' : 'd3']['fill']"
                                :fill-opacity="1" :stroke="'rgba(200, 200, 200, 0)'"></rect>
                            <text x="2" y="15" font-size="12">
                                {{ scope.row[xAxisValue == 0 ? "d2" : "d3"].v }}
                            </text>
                        </svg>
                    </template>
                </el-table-column>
            </el-table>
        </div>
    </div>
</template>

<script>
import { scaleLinear } from "d3-scale";
import { useDataStore } from "../stores/counter";
import { axisBottom, axisLeft } from "d3-axis";
import { select, selectAll } from "d3-selection";
import { drag } from "d3-drag";
import { polygonContains } from "d3-polygon";
import * as vsup from "vsup";
import { interpolateYlOrRd } from "d3-scale-chromatic";

export default {
    name: "PCV",
    props: [],
    data () {
        return {
            showTable: 0,
            elHeight: 0,
            elWidth: 0,
            smoothSelect: {},
            skipSelect: {},
            dot_data: [],
            tableData: [],
            xAxisValue: 0,
            yAxisValue: 0,
            xAxisOption: [{
                label: "CORR.",
                value: 0,
            },
            {
                label: "SHAP",
                value: 1,
            },
            ],
            yAxisOption: [{
                label: "RMSE",
                value: 0,
            },
            {
                label: "MAPE",
                value: 1,
            },
            ],
            lassoTag: 0,
            tbHeight: 0,
            tbWidth: 0,
            dtSelect: "sunspots",
            selectRowClass: "",
            localRowClass: "",
            legendTag: 0,
            select_all_id: {},
        };
    },
    methods: {
        /**
         * @description: refresh the table & scatter. clear all selections
         * @return {*}
         */
        refresh () {
            selectAll(".lasso").remove();
            selectAll(".corr_cir_out").remove();
            selectAll(".corr_cir_single").remove();
            selectAll(".black_select_row").attr("stroke-width", 0);
            selectAll(".representationSkipRect")
                .attr("opacity", 1)
                .attr("stroke-width", 0);
            this.localRowClass = "";

            this.tableData = this.calcTableData(this.dataSet, 1);
            selectAll(".corr_cir")
                .attr("opacity", (d) => {
                    return d.isShow ? 0 : 1;
                })
                .attr("fill", (d) => {
                    return d.fill;
                });
            const dataStore = useDataStore();
            dataStore.selectRowClass = 1;
        },
        /**
         * @description: determine whether to show or hide the legend
         * @return {*}
         */
        legendStatus () {
            if (this.legendTag == 0) {
                this.legendTag = 1;
            } else if (this.legendTag == 1) {
                this.legendTag = 0;
            }
        },
        /**
         * @description: select a prediction
         * @param {*} row a row in the table
         * @return {*}
         */
        selectPredict (row) {
            let td = row;
            this.localRowClass = td.uid;
            const dataStore = useDataStore();

            dataStore.selectResRow = {
                time_index: td.time,
                smooth: td.smooth,
                smooth_name: td.smooth_name,
                prediction_data: td.predict_data,
            };
            dataStore.rowSelectTag = 2;
            let select_dot = {};
            select_dot[td.uid] = 1;
            selectAll(".representationSkipRect")
                .attr("opacity", 0.15)
                .attr("stroke-width", 0);

            for (let i in select_dot) {
                select("#representation_" + i).attr("opacity", 1);
            }
            let tdata = [];
            if (selectAll(".corr_cir_out")["_groups"][0].length == 0) {
                tdata = [{
                    x: select("#corr_c" + td.uid).attr("cx"),
                    y: select("#corr_c" + td.uid).attr("cy"),
                    fill: select("#corr_c" + td.uid).attr("fill"),
                    uid: select("#corr_c" + td.uid).attr("uid"),
                },];
            } else {
                selectAll(".corr_cir_out").attr("class", (d) => {
                    if (d.uid == td.uid) {
                        tdata.push(d);
                    }
                    return "corr_cir_out";
                });
            }
            selectAll(".corr_cir_single").remove();

            select("#scatter")
                .append("g")
                .selectAll("#res_c")
                .attr("id", "res_c")
                .data(tdata)
                .enter()
                .append("circle")
                .attr("cx", (d) => d.x)
                .attr("cy", (d) => d.y)
                .attr("id", (d) => "corr_cir_single" + d.uid)
                .attr("class", "corr_cir_single")
                .attr("r", 7)
                .attr("stroke", "black")
                .attr("stroke-width", 2)
                .attr("fill", (d) => d.fill);
        },
        /**
         * @description: set the style of the selected row
         * @param {*} data
         * @return {*}
         */
        selectRowStyle (data) {
            if (data.row.uid == this.localRowClass) return "warning-row";
            return "";
        },
        /**
         * @description: setup the lasso tool
         * @return {*}
         */
        setupLasso () {
            let _this = this;
            let lasso_g = select("#scatter").append("g").attr("class", "lasso");
            let origin_node = lasso_g.append("circle").attr("id", "origin");
            let draw_path = lasso_g.append("path").attr("id", "drawn");
            let close_path = lasso_g.append("path").attr("id", "loop_close");

            let select_path = "";
            let target_circle;
            let closePathDistance = 100;

            let polygon = new Array();

            let dragStarted = function (event) {
                event;
                _this.lasso_t = 0;
            };
            let dragged = function (event) {
                let tx = event.x;
                let ty = event.y;
                if (select_path == "") {
                    select_path = select_path + "M " + tx + " " + ty;
                    target_circle = [event.x, event.y];
                    polygon.push([event.x, event.y]);
                } else {
                    select_path = select_path + "L " + tx + " " + ty;
                }
                polygon.push([tx, ty]);
                let distance = Math.sqrt(
                    Math.pow(tx - target_circle[0], 2) +
                    Math.pow(ty - target_circle[1], 2)
                );
                let close_draw_path = "M " + tx + " " + ty + " L " + target_circle[0] + " " + target_circle[1];
                draw_path.attr("d", select_path);
                close_path.attr("d", close_draw_path);
                if (distance < closePathDistance) {
                    close_path.attr("display", null);
                } else {
                    close_path.attr("display", "none");
                }
            };
            let dragEnded = async function (event) {
                origin_node.attr("display", "none");
                let tx = event.x;
                let ty = event.y;
                if (select_path == "") {
                    select_path = select_path + "M " + tx + " " + ty;
                    target_circle = [event.x, event.y];
                    polygon.push([event.x, event.y]);
                } else {
                    select_path = select_path + "L " + tx + " " + ty;
                }

                let distance = Math.sqrt(
                    Math.pow(tx - target_circle[0], 2) +
                    Math.pow(ty - target_circle[1], 2)
                );

                if (distance < 10) return;

                _this.lasso_t = 1;
                let select_dot = new Object();
                let select_info = new Array();
                // console.log()
                if (selectAll(".corr_cir_out")["_groups"][0].length == 0) {
                    for (let i in _this.dot_data) {
                        let dot_p = [_this.dot_data[i].x, _this.dot_data[i].y];
                        if (polygonContains(polygon, dot_p)) {
                            select_dot[_this.dot_data[i].uid] = 1;
                            _this.select_all_id[_this.dot_data[i].uid] = 1;
                            select_info.push(1);
                        } else {
                            select_info.push(0);
                        }
                    }
                    selectAll(".representationSkipRect").attr("opacity", 0.15);

                    for (let i in _this.select_all_id) {
                        select("#representation_" + i).attr("opacity", 1);
                    }

                    _this.tableData = _this.calcTableData(
                        _this.dataSet,
                        _this.select_all_id
                    );
                    selectAll(".corr_cir")
                        .attr("opacity", (d) => {
                            if (_this.select_all_id[d.uid] == 1) return 1;
                            else return d.isShow == 0 ? 0 : 0.5;
                        })
                        .attr("fill", (d) => {
                            if (_this.select_all_id[d.uid] == 1) return d.fill;
                            else return "#d9d9d9";
                        });
                } else {
                    let select_dot = new Object();
                    selectAll(".corr_cir_out")
                        .attr("fill", (d) => {
                            if (polygonContains(polygon, [d.x, d.y])) {
                                select_dot[d.uid] = 1;
                                return d.fill;
                            }
                            return "#d9d9d9";
                        })
                        .attr("opacity", (d) => {
                            if (polygonContains(polygon, [d.x, d.y])) {
                                return 1;
                            }
                            return 0.1;
                        });
                    selectAll(".representationSkipRect").attr("opacity", 0.15);
                    for (let i in select_dot) {
                        console.log(i);
                        select("#representation_" + i).attr("opacity", 1);
                    }
                    _this.tableData = _this.calcTableData(_this.dataSet, select_dot);
                }

                select_path = "";
                target_circle = [];
                closePathDistance = 100;
                polygon = new Array();
            };

            let dragL = drag()
                .on("start", dragStarted)
                .on("drag", dragged)
                .on("end", dragEnded);
            select("#modelExplainer").call(dragL);
        },
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
         * @description: calculate the table data
         * @param {*} data prediction information
         * @param {*} select_dot
         * @return {*}
         */
        calcTableData (data, select_dot) {
            let sdata = [];
            let id_cnt = 0;
            let max_rmse = -999999;
            let min_rmse = 99999;
            let max_corr = -999999;
            let min_corr = 999999;
            let max_shap = -999999;
            let min_shap = 999999;
            let all_corr_tag = 0;
            for (let i in data) {
                let startPos = 0;
                if (i > 3 && select_dot == 1) break;
                for (let j in data[i]) {
                    if (
                        parseFloat(data[i][j]["shap"]) > 1 ||
                        parseFloat(data[i][j]["shap"]) < -1
                    )
                        continue;
                    if (select_dot == 1 && j > 300) break;

                    if (data[i][j]["result_corr"] < 0 && this.dtSelect == "sunspots")
                        continue;
                    id_cnt++;
                    let predict_data = data[i][j]["predict_data"].split(" ");
                    let pre_data = [];
                    for (let k in predict_data) {
                        if (
                            predict_data[k] == ""
                        ) {
                            continue;
                        }
                        pre_data.push(
                            parseFloat(predict_data[k]) >= 0 ? parseFloat(predict_data[k]) : 0
                        );
                    }
                    let uid = data[i][j]["smooth"] + "_" + data[i][j]["skip"] + "_" + j;
                    if (select_dot != 1) {
                        if (select_dot[uid] != 1) {
                            continue;
                        }
                    }
                    let smooth_name = data[i][j]["Moving"];
                    let shap_tag = parseFloat(data[i][j]["shap"]) < 0 ? " (-)" : "";
                    let corr_tag = parseFloat(data[i][j]["result_corr"]) < 0 ? " (-)" : "";
                    if (corr_tag != "") {
                        all_corr_tag = 1;
                    }
                    if (this.smoothSelect[smooth_name] != 1 || this.skipSelect[parseInt(data[i][j]["skip"])] != 1)
                        continue;
                    sdata.push({
                        id: id_cnt,
                        predict_data: pre_data,
                        smooth: data[i][j]["smooth"],
                        skip: data[i][j]["skip"],
                        smooth_name: smooth_name,
                        time: j * data[i][j]["skip"] + startPos,
                        norm_corr: Math.abs(parseFloat(data[i][j]["result_corr"])).toFixed(4),
                        shap: Math.abs(parseFloat(data[i][j]["shap"])).toFixed(4),
                        shap_tag: shap_tag,
                        corr_tag: corr_tag,
                        rmse: parseFloat(data[i][j]["rmse"]).toFixed(2),
                        rmse_v: parseFloat(data[i][j]["rmse"]),
                        uid: data[i][j]["smooth"] + "_" + data[i][j]["skip"] + "_" + j,
                        cid: data[i][j]["smooth"] + "_" + data[i][j]["skip"],
                    });
                    max_rmse = Math.max(max_rmse, parseFloat(data[i][j]["rmse"]));
                    min_rmse = Math.min(min_rmse, parseFloat(data[i][j]["rmse"]));
                    max_corr = Math.max(max_corr, parseFloat(data[i][j]["result_corr"]));
                    min_corr = Math.min(min_corr, parseFloat(data[i][j]["result_corr"]));
                    max_shap = Math.max(max_shap, parseFloat(data[i][j]["shap"]));
                    min_shap = Math.min(min_shap, parseFloat(data[i][j]["shap"]));
                }

            }
            let barS = this.tbWidth - 82 - 62;
            let scale1 = scaleLinear([min_rmse, max_rmse], [0, barS / 2 - 5]);
            let scale2 = scaleLinear([min_corr, max_corr], [0, barS / 2 - 5]);
            let scale2_2 = scaleLinear([0, Math.max(Math.abs(min_corr), Math.abs(max_corr))], [0, (barS / 2 - 5) / 2]);
            let scale3 = scaleLinear([0, 1], [0, (barS / 2 - 5) / 2]);
            for (let i in sdata) {
                sdata[i]["d1"] = {
                    x: 0,
                    w: scale1(sdata[i]["rmse"]),
                    v: sdata[i]["rmse"],
                    fill: "orange",
                };
                let v2 = sdata[i]["norm_corr"].toString().slice(1);
                sdata[i]["d2"] = {
                    x: all_corr_tag == 1 ? sdata[i]["corr_tag"] == " (-)" ? (barS / 2 - 5) / 2 - scale2_2(Math.abs(sdata[i]["norm_corr"])) : (barS / 2 - 5) / 2 : 0,
                    w: all_corr_tag == 1 ? scale2_2(sdata[i]["norm_corr"]) : scale2(sdata[i]["norm_corr"]),
                    v: (sdata[i]["corr_tag"] == " (-)" ? "-" : "") + v2,
                    fill: sdata[i]["corr_tag"] == " (-)" ? "#3e539b" : "orange",
                };
                let v3 = sdata[i]["shap"].toString().slice(1);
                sdata[i]["d3"] = {
                    x: sdata[i]["shap_tag"] == " (-)" ?
                        (barS / 2 - 5) / 2 - scale3(Math.abs(sdata[i]["shap"])) :
                        (barS / 2 - 5) / 2,
                    w: scale3(Math.abs(sdata[i]["shap"])),
                    v: (sdata[i]["shap_tag"] == " (-)" ? "-" : "") + v3,
                    fill: sdata[i]["shap_tag"] == " (-)" ? "#3e539b" : "orange",
                };
            }
            return sdata;
        },
        /**
         * @description: calculate the scatter data
         * @param {*} data prediction information
         * @param {*} xAxisData Selected X-axis properties
         * @return {*} scatter data
         */
        calcScatter (data, xAxisData) {
            let sdata = [];
            let maxRmse = -999999;
            let minRmse = 999999;
            let maxNorm = -999999;
            let minNorm = 999999;
            let maxTime = -999999;
            let maxShap = -999999;
            let minShap = 999999;
            let id_cnt = 0;
            for (let i in data) {
                let startPos = 0;
                for (let j in data[i]) {
                    if (xAxisData == 1) {
                        if (data[i][j]["shap"] > 1 || data[i][j]["shap"] < -1) continue;
                    }
                    if (data[i][j]["result_corr"] < 0 && this.dtSelect == "sunspots")
                        continue;
                    let className = data[i][j]["smooth"] + "_" + data[i][j]["skip"];

                    let smooth_name = data[i][j]["Moving"];
                    let skip = parseInt(data[i][j]["skip"]);

                    if (this.smoothSelect[smooth_name] != 1 ||this.skipSelect[parseInt(data[i][j]["skip"])] != 1)
                        continue;
                    sdata.push({
                        id: i,
                        time: j * skip + startPos,
                        smooth: smooth_name,
                        skip: skip,
                        norm_corr: parseFloat(data[i][j]["result_corr"]),
                        rmse: parseFloat(data[i][j]["rmse"]),
                        shap: parseFloat(data[i][j]["shap"]),
                        isShow: Math.random() < (this.dtSelect == "sunspots" ? 0.2 : 0.05) ? 1 : 0,
                        id_cnt: id_cnt,
                        uid: data[i][j]["smooth"] + "_" + data[i][j]["skip"] + "_" + j,
                        cid: data[i][j]["smooth"] + "_" + data[i][j]["skip"],
                        class_name: className,
                    });
                    maxTime = Math.max(maxTime, j * skip + startPos);
                    maxRmse = Math.max(maxRmse, parseFloat(data[i][j]["rmse"]));
                    minRmse = Math.min(minRmse, parseFloat(data[i][j]["rmse"]));
                    maxNorm = Math.max(maxNorm, parseFloat(data[i][j]["result_corr"]));
                    minNorm = Math.min(minNorm, parseFloat(data[i][j]["result_corr"]));
                    minShap = Math.min(minShap, parseFloat(data[i][j]["shap"]));
                    maxShap = Math.max(maxShap, parseFloat(data[i][j]["shap"]));
                    id_cnt++;
                }
            }
            let quantization2 = vsup
                .quantization()
                .branching(2)
                .layers(4)
                .valueDomain([minRmse, maxRmse])
                .uncertaintyDomain([maxNorm, minNorm]);
            let heatColor = interpolateYlOrRd;
            let heatScale = vsup.scale().quantize(quantization2).range(heatColor);

            let rmseScale = scaleLinear([minRmse, maxRmse], [this.elHeight - 20, 5]);
            let normScale = scaleLinear(
                [minNorm > 0 ? 0 : minNorm, maxNorm], [30, this.elWidth - 20]
            );
            let shapScale = scaleLinear([minShap, maxShap], [30, this.elWidth - 20]);
            var legend = vsup.legend.arcmapLegend();

            selectAll("#vsup_legend_g_s").remove();
            legend.scale(heatScale)
                .size(140)
                .x(70)
                .y(40)
                .vtitle("RMSE")
                .utitle("CORR.");
            select("#legend_g_s")
                .append("g")
                .attr("id", "vsup_legend_g_s")
                .call(legend);

            let xAxis = axisBottom(xAxisData == 1 ? shapScale : normScale).ticks(10);
            let yAxis = axisLeft(rmseScale).ticks(10);

            for (let i in sdata) {
                sdata[i].x = xAxisData == 1 ? shapScale(sdata[i].shap) : normScale(sdata[i].norm_corr);
                sdata[i].y = rmseScale(sdata[i].rmse);
                sdata[i].fill = heatScale(sdata[i].rmse, sdata[i].norm_corr);
            }
            selectAll(".corr_cir").remove();
            select("#scatter")
                .append("g")
                .selectAll("#res_c")
                .attr("id", "res_c")
                .data(sdata, (d) => {
                    if (d.isShow == 1) {
                        return d;
                    }
                })
                .enter()
                .append("circle")
                .attr("cx", (d) => d.x)
                .attr("cy", (d) => d.y)
                .attr("id", (d) => "corr_c" + d.uid)
                .attr("class", "corr_cir")
                .attr("r", 2)
                .attr("fill", (d) => d.fill)
                .attr("opacity", (d) => d.isShow)
                .attr("cursor", "pointer")
                .on("mouseover", (e, d) => {
                    select("#corr_c" + d.id_cnt).attr("r", d.isShow == 1 ? 5 : 1);
                })
                .on("mouseout", (e, d) => {
                    select("#corr_c" + d.id_cnt).attr("r", 2);
                });

            selectAll("#dotAxis_g").remove();
            select("#x_axis_g")
                .append("g")
                .attr("id", "dotAxis_g")
                .attr("transform", `translate(0, ${this.elHeight - 20})`)
                .call(xAxis)
                .call((g) =>
                    g.selectAll(".title")
                        .data([xAxisData == 1 ? "SHAP." : "CORR."])
                        .join("text")
                        .attr("class", "title")
                        .attr("x", this.elWidth - 20)
                        .attr("y", 19)
                        .attr("fill", "currentColor")
                        .attr("text-anchor", "middle")
                        .attr("font-size", "14px")
                        .text((d) => d)
                );
            select("#y_axis_g")
                .append("g")
                .attr("id", "dotAxis_g")
                .attr(
                    "transform",
                    `translate(${xAxisData == 1 ? shapScale(0) : normScale(0)}, 0)`
                )
                .call(yAxis)
                .call((g) =>
                    g.selectAll(".title")
                        .data(["RMSE"])
                        .join("text")
                        .attr("class", "title")
                        .attr("x", 22)
                        .attr("y", 15)
                        .attr("fill", "currentColor")
                        .attr("text-anchor", "middle")
                        .attr("font-size", "14px")
                        .text((d) => d)
                );

            return sdata;
        },
        /**
         * @description: data processing
         * @param {*} data
         * @return {*}
         */
        dataDivide (data) {
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
        dataDivide (data) {
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
        dataConvert (data) {
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
    created () { },
    mounted () {
        this.elHeight = this.$refs.modelExplainer.offsetHeight;
        this.elWidth = this.elHeight + 20;
        this.tbHeight = this.$refs.modelTable.offsetHeight;
        this.tbWidth = this.$refs.modelTable.offsetWidth;

        const dataStore = useDataStore();
        let _this = this;

        /**
         * @description: watch the data changes in the store
         * @return {*}
         */        
        dataStore.$subscribe((mutations) => {
            // init the view
            if (mutations.events.key == 'system_data') {
                this.smoothSelect = dataStore.smooth;
                this.skipSelect = dataStore.skip;
                this.showTable = 1;
                this.dtSelect = dataStore.system_data.file_name;
                let result_data = JSON.parse(dataStore.system_data.result_data);
                let res_data = this.dataDivide(this.dataConvert(result_data));
                let dataSet = [];
                for (let i in res_data) {
                    dataSet.push(res_data[i].data);
                }
                this.dataSet = dataSet;
                this.dot_data = this.calcScatter(dataSet, this.xAxisValue);
                this.tableData = this.calcTableData(dataSet, 1);
                this.setupLasso();
            }
            if (dataStore.selectRowClass != this.selectRowClass) {
                this.selectRowClass = dataStore.selectRowClass;
                if (dataStore.selectRowClass != 1) {
                    let select_dot = {};
                    for (let i in _this.dot_data) {
                        if (_this.dot_data[i].cid == dataStore.selectRowClass) {
                            select_dot[_this.dot_data[i].uid] = 1;
                        }
                    }
                    this.tableData = this.calcTableData(this.dataSet, select_dot);
                    console.log(this.tableData);
                } else {
                    this.tableData = this.calcTableData(this.dataSet, 1);
                }
            }

        });
    },
    watch: {
        xAxisValue () {
            this.dot_data = this.calcScatter(this.dataSet, this.xAxisValue);
        },
    },
};
</script>

<style>

.cell {
    color: black;
}

.lasso path {
    stroke: #2378ae;
    stroke-width: 3;
    stroke-dasharray: 4, 4;
}

.lasso #drawn {
    fill-opacity: 0.05;
}

.lasso #loop_close {
    fill: none;
    stroke-dasharray: 4, 4;
}

.lasso #origin {
    fill: rgb(180, 180, 180);
    fill-opacity: 0.5;
}

.el-table .cell {
    padding: 0px;
    text-align: left;
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

/*chrome--------------------------------------------end*/</style>
