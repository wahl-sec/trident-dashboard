# **Trident Dashboard**

## **Description**
Trident Dashboard aggregates and visualizes the `Trident` daemons, plugins and results produced by [Trident IDS](https://gitlab.com/wahl-sec/trident).

The dashboard is a single-page application that uses `Chart.js` to visualize the results and other runtime information regarding the connected `Trident` daemons.

If a dashboard is defined when running `Trident`, a connect request from the `Trident` daemon is sent to the dashboard to establish a connection. With the initial connection we also send information like what plugins are running. After each iteration of results from the plugins that are being run in the daemon we send the results to the dashboard. The results published are stored and visualized using `Chart.js`. 