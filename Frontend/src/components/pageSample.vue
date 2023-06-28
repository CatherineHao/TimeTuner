<!--
 * @Description: 
 * @Author: Qing Shi
 * @Date: 2023-01-10 21:20:01
 * @LastEditTime: 2023-01-10 21:24:05
-->
<template>
    <div class="frameworkTitle">
        <div class="title"></div>
        <p class="titleTriangle"></p>
    </div>
    <div class="frameworkBody">
        <div ref="svgBody" style="height: 100%; width: 100%;">
            <svg id="svgBody" height="100%" width="100%">
                
            </svg>
        </div>
    </div>
</template>
<script>
export default {
    name: 'ExView',
    props: [],
    data() {
        return {
            elHeight: 0,
            elWidth: 0,
        }
    },
    methods: {
        translate(x, y, deg) {
            return `translate(${x}, ${y}) rotate(${deg})`;
        }
    },
    created() {
    },
    mounted() {
        this.elHeight = this.$refs.svgBody.offsetHeight;
        this.elWidth = this.$refs.svgBody.offsetWidth;
    },
}
</script>
<style scoped>
*,
*::before,
*::after {
    font-weight: bold;
}
</style>
