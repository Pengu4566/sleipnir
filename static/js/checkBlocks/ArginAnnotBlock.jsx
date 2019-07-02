import React from "react";

export default class ArginAnnotBlock extends React.Component {
  render() {
    if (this.props.name == "There is no argument in this project.") {
      return (
        <div className="single_check">
          <h3>Argument Explanation in Annotation</h3>
          <div className="check_explain">
            <p>
              Argument should be at least mentioned in the annotation of the
              workflow.
            </p>
            <p>There is no argument in this project.</p>
          </div>
        </div>
      );
    } else if (this.props.name == "[The file you uploaded is not completed.]") {
      return (
        <div className="single_check">
          <h3>Argument Explanation in Annotation</h3>
          <div className="check_explain">
            <p>
              Argument should be at least mentioned in the annotation of the
              workflow.
            </p>
            <p>
              The file you uploaded is not complete, therefore we could not
              perform this check on it.
            </p>
          </div>
        </div>
      );
    } else if (this.props.name == "[Not evaluated]") {
      return <div />;
    } else {
      return (
        <div className="single_check">
          <h3>Argument Explanation in Annotation</h3>
          <div className="check_explain">
            <p>
              Argument should be at least mentioned in the annotation of the
              workflow. Arguments that are not even mentioned in the annotation
              include:
            </p>
            <p>{this.props.name}</p>
          </div>
        </div>
      );
    }
  }
}
