import React from "react";
import ReactTable from "react-table";
import "react-table/react-table.css";
import _ from "lodash";

export default class ActivityStatsBlock extends React.Component {
  constructor() {
    super();
    this.state = { collapse: false, byProject: false };
  }
  toggle() {
    this.setState(state => ({ collapse: !state.collapse }));
  }
  switchGroupBy() {
    this.setState(state => ({ byProject: !state.byProject }));
  }
  render() {
    if (
      this.props.name.data == ["There is no activity in files you uploaded."]
    ) {
      return (
        <div className="act_stat">
          <h3 onClick={this.toggle.bind(this)}>Activity Statistics</h3>
          <div
            className="check_explain"
            style={{ display: this.state.collapse ? "block" : "none" }}
          >
            <p>There is no activity in files you uploaded.</p>;
          </div>
        </div>
      );
    } else {
      if (this.state.byProject) {
        const columns = [
          {
            Header: "Activity Type",
            accessor: "activityType"
          },
          {
            Header: "Time Appeared",
            accessor: "count"
          },
          {
            Header: "From Project",
            accessor: "projectId"
          }
        ];
        return (
          <div className="act_stat">
            <h3 onClick={this.toggle.bind(this)}>Activity Statistics</h3>
            <div
              className="check_explain"
              style={{ display: this.state.collapse ? "block" : "none" }}
            >
              <button id="groupBy" onClick={this.switchGroupBy.bind(this)}>
                By File
              </button>

              <ReactTable
                columns={columns}
                data={this.props.name.data.byProject}
                filterable
                defaultSorted={[
                  {
                    id: "count",
                    desc: true
                  }
                ]}
              />
            </div>
          </div>
        );
      } else {
        const columns = [
          {
            Header: "Activity Type",
            accessor: "activityType"
          },
          {
            Header: "Time Appeared",
            accessor: "count"
          },

          {
            Header: "From File",
            accessor: "filePath"
          },
          {
            Header: "From Project",
            accessor: "projectId"
          }
        ];
        return (
          <div className="act_stat">
            <h3 onClick={this.toggle.bind(this)}>Activity Statistics</h3>
            <div
              className="check_explain"
              style={{ display: this.state.collapse ? "block" : "none" }}
            >
              <button id="groupBy" onClick={this.switchGroupBy.bind(this)}>
                By Project
              </button>
              <ReactTable
                columns={columns}
                data={this.props.name.data.byFile}
                filterable
                defaultSorted={[
                  {
                    id: "count",
                    desc: true
                  }
                ]}
              />
            </div>
          </div>
        );
      }
    }
  }
}
