import React from "react";
import ReactDOM from "react-dom";
import style from "../css/table_expansion_result_page";
// import * as bstree_styles from "../css/bstree";
// import * as jquery from "../js/jquery.bstree";
// import CheckButtons from "./CheckButtons";
// import ImproperNamedVarBlock from "./checkBlocks/ImproperNamedVarBlock";
// import UnusedVarBlock from "./checkBlocks/UnusedVarBlock";
// import ImproperNamedArgBlock from "./checkBlocks/ImproperNamedArgBlock";
// import UnusedArgBlock from "./checkBlocks/UnusedArgBlock";
// import ImproperNamedActBlock from "./checkBlocks/ImproperNamedActBlock";
// import NoSsExpBlock from "./checkBlocks/NoSsExpBlock";
// import NotAnnotWfBlock from "./checkBlocks/NotAnnotWfBlock";
// import NoLMExpBlock from "./checkBlocks/NoLMExpBlock";
// import ArginAnnotBlock from "./checkBlocks/ArginAnnotBlock";
import JsonLogBlock from "./checkBlocks/JsonLogBlock";
import Table1ContentHTML from "./checkBlocks/Table1Content";
import ActivityStatsBlock from "./checkBlocks/ActivityStats";
import ActStatsChecks from "./checkBlocks/ActStatsChecks";
import SelectorTable from "./checkBlocks/SelectorTable";

// ReactDOM.render(
//   <CheckButtons
//     naming={window.NamingScore}
//     usage={window.UsageScore}
//     doc={window.DocScore}
//   />,
//   document.getElementById("all_categories_content")
// );

// ReactDOM.render(
//   <ImproperNamedVarBlock name={window.improperNamedVar} />,
//   document.getElementById("VarName")
// );

// ReactDOM.render(
//   <UnusedVarBlock name={window.unusedVar} />,
//   document.getElementById("VarUsage")
// );

// ReactDOM.render(
//   <ImproperNamedArgBlock name={window.improperNamedArg} />,
//   document.getElementById("ArgName")
// );

// ReactDOM.render(
//   <UnusedArgBlock name={window.unusedArg} />,
//   document.getElementById("ArgUsage")
// );

// ReactDOM.render(
//   <ImproperNamedActBlock name={window.improperNamedAct} />,
//   document.getElementById("ActName")
// );

// ReactDOM.render(
//   <NoSsExpBlock name={window.noSsExp} />,
//   document.getElementById("ExpSs")
// );

// ReactDOM.render(
//   <NotAnnotWfBlock name={window.notAnnotWf} />,
//   document.getElementById("WfAnnot")
// );

// ReactDOM.render(
//   <NoLMExpBlock name={window.noLMExp} />,
//   document.getElementById("ExpLM")
// );

// ReactDOM.render(
//   <ArginAnnotBlock name={window.missingArg} />,
//   document.getElementById("ArginAnnot")
// );

ReactDOM.render(
  <JsonLogBlock name={window.projectOverviewTableData} />,
  document.getElementById("projectOverviewTable")
);

ReactDOM.render(
  <Table1ContentHTML name={window.table1Data} />,
  document.getElementById("table1")
);

ReactDOM.render(
  <ActivityStatsBlock name={window.actStats} />,
  document.getElementById("actStatsTable")
);

// ReactDOM.render(
//   <ActStatsChecks name={window.actStats} />,
//   document.getElementById("actStatsChecks")
// );

ReactDOM.render(
  <SelectorTable name={window.selectorTableData} />,
  document.getElementById("selectorTable")
);
