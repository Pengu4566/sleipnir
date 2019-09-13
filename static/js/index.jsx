import React from "react";
import ReactDOM from "react-dom";
import * as table_styles from "../css/table_expansion_result_page";
import * as bstree_styles from "../css/bstree";
import * as jquery from "../js/jquery.bstree";
import CheckButtons from "./CheckButtons";
import ImproperNamedVarBlock from "./checkBlocks/ImproperNamedVarBlock";
import UnusedVarBlock from "./checkBlocks/UnusedVarBlock";
import ImproperNamedArgBlock from "./checkBlocks/ImproperNamedArgBlock";
import UnusedArgBlock from "./checkBlocks/UnusedArgBlock";
import ImproperNamedActBlock from "./checkBlocks/ImproperNamedActBlock";
import NoSsExpBlock from "./checkBlocks/NoSsExpBlock";
import NotAnnotWfBlock from "./checkBlocks/NotAnnotWfBlock";
import NoLMExpBlock from "./checkBlocks/NoLMExpBlock";
import ArginAnnotBlock from "./checkBlocks/ArginAnnotBlock";
import JsonLogBlock from "./checkBlocks/JsonLogBlock";
import ActivityStatsBlock from "./checkBlocks/ActivityStats";
import SelectorEvalBlock from "./checkBlocks/SelectorEvalBlock";

// ReactDOM.render(
//   <CheckButtons
//     naming={window.NamingScore}
//     usage={window.UsageScore}
//     doc={window.DocScore}
//   />,
//   document.getElementById("all_categories_content")
// );

ReactDOM.render(
  <ImproperNamedVarBlock name={window.improperNamedVar} />,
  document.getElementById("VarName")
);

ReactDOM.render(
  <UnusedVarBlock name={window.unusedVar} />,
  document.getElementById("VarUsage")
);

ReactDOM.render(
  <ImproperNamedArgBlock name={window.improperNamedArg} />,
  document.getElementById("ArgName")
);

ReactDOM.render(
  <UnusedArgBlock name={window.unusedArg} />,
  document.getElementById("ArgUsage")
);

ReactDOM.render(
  <ImproperNamedActBlock name={window.improperNamedAct} />,
  document.getElementById("ActName")
);

ReactDOM.render(
  <NoSsExpBlock name={window.noSsExp} />,
  document.getElementById("ExpSs")
);

ReactDOM.render(
  <NotAnnotWfBlock name={window.notAnnotWf} />,
  document.getElementById("WfAnnot")
);

ReactDOM.render(
  <NoLMExpBlock name={window.noLMExp} />,
  document.getElementById("ExpLM")
);

ReactDOM.render(
  <JsonLogBlock name={window.projectDetail} />,
  document.getElementById("JsonLog")
);

ReactDOM.render(
  <ArginAnnotBlock name={window.missingArg} />,
  document.getElementById("ArginAnnot")
);

ReactDOM.render(
  <ActivityStatsBlock name={window.activityStats} />,
  document.getElementById("ActivityStats")
);

ReactDOM.render(
  <SelectorEvalBlock name={window.selectorEval} />,
  document.getElementById("SelectorEvaluation")
);
