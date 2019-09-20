import React from "react";
import ReactDOM from "react-dom";
import style from "../css/table_expansion_result_page";
import JsonLogBlock from "./checkBlocks/JsonLogBlock";
import Table1ContentHTML from "./checkBlocks/Table1Content";
import ActivityStatsBlock from "./checkBlocks/ActivityStats";
import ActStatsChecks from "./checkBlocks/ActStatsChecks";
import SelectorTable from "./checkBlocks/SelectorTable";
import Table1Filters from "./checkBlocks/Table1Filters";

ReactDOM.render(
  <JsonLogBlock name={window.projectOverviewTableData} />,
  document.getElementById("projectOverviewTable")
);

ReactDOM.render(
  <Table1Filters name={window.table1Data} />,
  document.getElementById("table1Filters")
);

ReactDOM.render(
  <Table1ContentHTML name={window.table1Data.data} />,
  document.getElementById("table1")
);

ReactDOM.render(
  <ActivityStatsBlock name={window.actStats} />,
  document.getElementById("actStatsTable")
);

ReactDOM.render(
  <ActStatsChecks name={window.actStats} />,
  document.getElementById("actStatsChecks")
);

ReactDOM.render(
  <SelectorTable name={window.selectorTableData} />,
  document.getElementById("selectorTable")
);
