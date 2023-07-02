<!--
 * @Description: Main Interface
 * @Author: Qing Shi
 * @Date: 2023-06-29 10:17:17
 * @LastEditors: Qing Shi
 * @LastEditTime: 2023-07-01 21:42:28
-->
<template> 
    <div id="navBar">
        <img src="../assets/logo/logo.png" width="35" alt="" style="margin-top: 5px;">
        <span style="font-weight: 800; padding-left: 10px; margin-bottom: 100px; position: absolute;">TimeTuner</span>
        <span style="position: absolute; right: 10px;">Diagnosing Time Representations for Time-Series Forecasting with Counterfactual Explanations</span> 
    </div>
    <div style="height: calc(96vh - 0px); width: calc(100% - 0px);">
        <div class="framework" id="controlPanel"
            style="position: absolute; left: calc(5px); top: calc(5px); height: calc(27vw); width: calc(15vw + 10px);">
            <ProfileView />
        </div>

        <div class="framework" id="DistributionView"
            style="position: absolute; left: calc(15vw - 5px + 30px);  top: calc(5px); height: calc(27vw); width: calc(27vw - 30px);">
            <VariableInspectorView/>
        </div>
        <div class="framework" id="DataTransformation"
            style="position: absolute; right: 5px; top: calc(5px); height: calc((96vh - 10px) * .45 - 10px); width: calc(58vw - 10px);">
            <TemporalView/>
        </div>
        <div class="framework" id="DataTransformation"
            style="position: absolute; right: 5px; top: calc((96vh - 10px) * .45 + 5px); height: calc((96vh - 10px) * .55 - 0px); width: calc(58vw - 10px);">
            <RepresentationView />
        </div>
        <div class="framework" id="ModelExplainer"
            style="position: absolute; left: calc(5px); top: calc(27vw + 15px); height: calc(96vh - 27vw - 20px); width: calc(42vw - 10px);">
            <PredictionComparatorView/>
        </div>
    </div>
</template>
<script>
import PredictionComparatorView from './PredictionComparatorView.vue';
import TemporalView from './TemporalView.vue';
import ProfileView from './ProfileView.vue';
import VariableInspectorView from './VariableInspectorView.vue';
import RepresentationView from './RepresentationView.vue';
export default {
    name: "APP",
    props: ["msgH"],
    data() {
        return {
            msg1: "Hello, main!"
        };
    },
    methods: {},
    created() {
    },
    mounted() {
    },
    components: { PredictionComparatorView, TemporalView, ProfileView, VariableInspectorView, RepresentationView }
}
</script>
<style>
.framework {
    border: 0px solid rgb(105, 119, 122);
    background-color: white;
    border-radius: 5px;
}

.framework .frameworkTitle {
    height: 40px;
}

.framework .frameworkBody {
    height: calc(100% - 50px);
    padding: 10px 10px 5px 10px;
}

.framework .frameworkTitle .title {
    float: left;
    width: fit-content;

    background-color: rgb(105, 119, 122);
    height: 35px;

    font-weight: 600;
    font-size: 24px;
    color: white;
    padding-left: 10px;
    padding-right: 3px;
    font-family: 'KoHo';
    line-height: 35px;
}

.framework .frameworkTitle .titleTriangle {
    float: left;
    width: 0;
    height: 0;
    border-color: transparent rgb(105, 119, 122);
    border-width: 0px 0px 35px 35px;
    border-style: solid;
}

#navBar {
    background-color: #4d4d4d;
    text-align: left;
    font-weight: bold;
    color: white;
    font-size: 28px;
    height: calc(4%);
    padding-top: 0.2%;
    padding-bottom: 0.5%;
    padding-left: 10px;
    font-family: 'KoHo', 'Avenir', Helvetica, Arial, sans-serif;
}
</style>
