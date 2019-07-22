import React from "react";
import ReactTable from "react-table";
import "react-table/react-table.css";

export default class NotAnnotWfBlock extends React.Component {
  render() {
    if (this.props.name == []) {
      return (
        <div className="single_check">
          <h3>Workflow Annotation</h3>
          <div className="check_explain">
            <p>
              Workflow annotation is evaluated by checking if all invoked
              workflow is annotated.
            </p>
            <p>There is no workflow that is invoked but not annotated.</p>
          </div>
        </div>
      );
    } else if (this.props.name == ["Not evaluated"]) {
      return <div />;
    } else if (this.props.name == ["The file you uploaded is not completed."]) {
      return (
        <div className="single_check">
          <h3>Workflow Annotation</h3>
          <div className="check_explain">
            <p>
              Workflow annotation is evaluated by checking if all invoked
              workflow is annotated. An invoked workflow should always be
              annotated. However, the file you uploaded is not completed, so we
              cannot analyze workflow annotation for you.
            </p>
          </div>
        </div>
      );
    } else if (
      this.props.name == ["There is no invoked workflow in your project."]
    ) {
      return (
        <div className="single_check">
          <h3>Workflow Annotation</h3>
          <div className="check_explain">
            <p>
              Workflow annotation is evaluated by checking if all invoked
              workflow is annotated.
            </p>
            <p>There is no invoked workflow in your project.</p>
          </div>
        </div>
      );
    } else {
      const columns = [
        {
          Header: "Workflow ID",
          accessor: "index"
        },
        {
          Header: "Workflow Path",
          accessor: "workflowName"
        }
      ];
      return (
        <div className="single_check">
          <h3>Workflow Annotation</h3>
          <div className="check_explain">
            <p>
              Workflow annotation is evaluated by checking if all invoked
              workflow is annotated. An invoked workflow should always be
              annotated. Such workflows that are not annotated include:
            </p>
            <ReactTable columns={columns} data={this.props.name.data} />
          </div>
        </div>
      );
    }
  }
}
