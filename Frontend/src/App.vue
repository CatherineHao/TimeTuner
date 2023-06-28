<!--
 * @Description: 
 * @Author: Qing Shi
 * @Date: 2022-11-20 18:21:36
 * @LastEditTime: 2023-01-10 16:36:27
-->
<script setup>
import { RouterLink, RouterView } from "vue-router";
</script>

<template>
  <div id="app" 
    style="height: calc(100vh - 20px)">
    <RouterView />
  </div>
</template>

<style>
@import './common/font.css';
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  height: 100%;
  width: 100%;
}

.mini_head {
  /* background: rgb(243,243,243); */
  /* background: #E5EEF8 ; */
  width: 100%;
  height: 40px;
  padding: 5px;
  display: flex;
  box-sizing: border-box;
}

.mini_title {
  font-family: "monospace";
  width: 100%;
  height: 30px;
  font-size: 18px;
  /* color: #fff; */
  /* padding-left: 3px; */
  /* display: table-cell; */
  font-weight: bold;
  /* vertical-align: middle;
        background: #E5EEF8; */
        
  /* border-radius: 3px; */
  border-top-right-radius: 2px;
  border-top-left-radius: 2px;

  /* background-image: linear-gradient(
    to right,
    #418d8e,
    rgb(102, 173, 179),
    #e8d7cc
  ); */
  line-height: 30px;
}

.boundary {
  border-style: dashed;
  border-color: #d3dce6;
  border-width: 1px;
  /* border-color: rgb(72, 143, 143); */
}

.el-table .warning-row {
  background: #a6cee3;
  
  /* background-image: linear-gradient(
    to right,
    white, 70%,
    #B6D0D1
  ); */
}

.boundary {
  /*border-style: dashed;*/
  border-style: solid;
  /* border-color: rgb(72, 143, 143); */
  border-width: 1px;
  border-radius: 3px;
}
</style>
