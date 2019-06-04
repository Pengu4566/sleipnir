import React from "react";
import ReactDOM from "react-dom";
import ImproperNamedVarBlock from "./checkBlocks/ImproperNamedVarBlock";
import UnusedVarBlock from "./checkBlocks/UnusedVarBlock";
import ImproperNamedArgBlock from "./checkBlocks/ImproperNamedArgBlock";
import UnusedArgBlock from "./checkBlocks/UnusedArgBlock";
import ImproperNamedActBlock from "./checkBlocks/ImproperNamedActBlock";
import NoSsExpBlock from "./checkBlocks/NoSsExpBlock";
import NotAnnotWfBlock from "./checkBlocks/NotAnnotWfBlock";
import NoLMExpBlock from "./checkBlocks/NoLMExpBlock";

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
