import React from "react";
import ReactDOM from "react-dom";
import style from "../css/table_expansion_result_page";
import JsonLogBlock from "./checkBlocks/JsonLogBlock";
import ActivityStatsBlock from "./checkBlocks/ActivityStats";
import SelectorTable from "./checkBlocks/SelectorTable";
import Table1 from "./checkBlocks/Table1Filters";

ReactDOM.render(
  <JsonLogBlock name={window.projectOverviewTableData} />,
  document.getElementById("projectOverviewTable")
);

ReactDOM.render(
  <Table1 name={window.table1Data} />,
  document.getElementById("table1")
);

ReactDOM.render(
  <ActivityStatsBlock name={window.actStats} />,
  document.getElementById("actStatsTable")
);

ReactDOM.render(
  <SelectorTable name={window.selectorTableData} />,
  document.getElementById("selectorTable")
);
