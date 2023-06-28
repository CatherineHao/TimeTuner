/*
 * @Description: 
 * @Author: Qing Shi
 * @Date: 2022-09-17 23:36:36
 * @LastEditTime: 2023-02-02 15:02:39
 */
import { fetchHello } from "../service/module/dataService";
import { ref, computed } from "vue";
import { defineStore } from "pinia";

// export const useCounterStore = defineStore("counter", {
//   const count = ref(0);
//   const doubleCount = computed(() => count.value * 2);
//   function increment() {
//     count.value++;
//   }

//   return { count, doubleCount, increment };
// });

export const useDataStore = defineStore("dataStore", {
  state: () => {
    return {
      msg: 'Hello, Vue SQ',
      model: null,
      selectDot: {tag: 0,data: []},
      select_row: null,
      dataSelect: 'aaa',
      selectRepresentation: { 
        tag: 0,
        data: []
      },
      selectRowClass: '',
      selectSmooth: [],
      selectResRow: {
        time_index: 0,
        smooth: '',
        prediction_data: []
      },
      rowSelectTag: 0,
      changeTag: '',
      skip: {},
      smooth: {}
    }
  },
  actions: {
    fetchHello () {
      const st = new Date();
      fetchHello({}, resp => {
        this.msg = resp;
        console.log("Fetch Hello Time: ", st - new Date());
      })
    }
  }
})