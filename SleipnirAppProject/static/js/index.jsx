import React from "react";
import ReactDOM from "react-dom";
import ImproperNamedVarBlock from "./ImproperNamedVarBlock";
import UnusedVarBlock from "./UnusedVarBlock";
import ImproperNamedArgBlock from "./ImproperNamedArgBlock";
import ImproperNamedActBlock from "./ImproperNamedActBlock";
import NoSsExpBlock from "./NoSsExpBlock";
import NotAnnotWfBlock from "./NotAnnotWfBlock";
import NoLMExpBlock from "./NoLMExpBlock";

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
