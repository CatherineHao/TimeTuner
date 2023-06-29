<!--
 * @Description: 
 * @Author: Qing Shi
 * @Date: 2022-09-17 23:36:36
 * @LastEditTime: 2023-02-13 11:02:16
-->
<template>
  <div class="common-layout" style="width: 100%; height: 100vh; background-color: #e6e6e6;" v-loading="!initSign" :element-loading-text="loadingText"
        element-loading-background="rgba(0, 0, 0, 0.8)">
    <Main :msgH="msgH"/>
    <!-- #e6e6e6 -->
  </div>
</template>

<script>
import Main from '../components/Main.vue';
import { useDataStore } from "../stores/counter";


export default {
  name: "home_view",
  data() {
    return {
      msgH: null,
      timeData: null,
      sliceData: null,
      basicData: null
    };
  },
  computed: {
    initSign() {
      return 1;
    },
    loadingText() {
      return "Loading"
    }
  },
  mounted() {
    // const dataStore = useDataStore();
    // dataStore.tag = 1;
    
    // const dataStore = useDataStore();
    // dataStore.fetchHello();
    // this.msgH = dataStore.msg;
    this.msgH = 1;
  },
  methods: {
    fetchData() {
    }
  },
  components: { Main }
};
</script>
<style scoped>

.boundary {
        /*border-style: dashed;*/
        border-style: solid;
        border-color: #d3dce6;
        border-width: 0.5px;
        border-radius: 3px;
    }
</style>
