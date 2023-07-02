<!--
 * @Author: CatherineHao 1512769550@qq.com
 * @Date: 2023-06-29 21:38:50
 * @LastEditors: CatherineHao 1512769550@qq.com
 * @LastEditTime: 2023-07-02 14:58:54
 * @FilePath: \undefinede:\VIS23\vis_github\TimeTuner\README.md
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
# TimeTuner - Diagnosing Time Representations for Time-Series Forecasting with Counterfactual Explanations

![interface](interface.png "The interface of TimeTuner. It consists of five main views: Profile View, Variable Inspector View, Temporal View, Representation View and Prediction Comparator View")

### Summary:
**TimeTuner** is a general visual analytics framework. which is designed to help analysts understand how model behaviors are associated with localized correlations, stationarity, and granularity of time-series representations. 
In our work, we instantiate TimeTuner with two transformation methods of smoothing and sampling, and demonstrate its applicability  on real-world time-series forecasting of univariate sunspots and multivariate air pollutants.

### Dependencies
The following environments and packages are required to run this project:
- **backend:**
  - Python: version 3.8 or higher
  - SHAP: version 0.41.0
  - pandas: version 1.5.3
  - tensorflow: version 2.10.0
  - keras: version 2.10.0
  - scikit-learn: version 1.2.2
  - numpy: version 1.24.3
  - Flask: version 2.2.0
- **frontend:**
  - Vue.js 3
  
Make sure to have Python 3.8 or higher version installed before proceeding with the packages installation.

### Recommended IDE Setup
[VSCode](https://code.visualstudio.com/) + [Python 3.9](https://www.python.org/downloads/release/python-390/) + [Flask 2.2](https://flask.palletsprojects.com/en/2.2.x) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin).