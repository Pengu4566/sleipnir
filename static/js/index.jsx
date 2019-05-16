import React from "react";
import ReactDOM from "react-dom";
import ImproperNamedVarBlock from "./checkBlocks/ImproperNamedVarBlock";
import UnusedVarBlock from "./checkBlocks/UnusedVarBlock";
import ImproperNamedArgBlock from "./checkBlocks/ImproperNamedArgBlock";
import ImproperNamedActBlock from "./checkBlocks/ImproperNamedActBlock";
import NoSsExpBlock from "./checkBlocks/NoSsExpBlock";
import NotAnnotWfBlock from "./checkBlocks/NotAnnotWfBlock";
import NoLMExpBlock from "./checkBlocks/NoLMExpBlock";

ReactDOM.render(
  <ImproperNamedVarBlock name={window.improperNamedVar} />,
  document.getElementById("varname")
);

ReactDOM.render(
  <UnusedVarBlock name={window.unusedVar} />,
  document.getElementById("varusage")
);

ReactDOM.render(
  <ImproperNamedArgBlock name={window.improperNamedArg} />,
  document.getElementById("argname")
);

ReactDOM.render(
  <ImproperNamedActBlock name={window.improperNamedAct} />,
  document.getElementById("actname")
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
  document.getElementById("expLM")
);
