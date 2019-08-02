import React from "react";
import ReactTable from "react-table";
import "react-table/react-table.css";
import _ from "lodash";

export default class ActivityStatsBlock extends React.Component {
  constructor(props) {
    super(props);
    this.state = { collapse: false, byProject: false };
    console.log(this.props.name);
  }
  toggle() {
    this.setState(state => ({ collapse: !state.collapse }));
  }
  switchGroupBy() {
    this.setState(state => ({ byProject: !state.byProject }));
  }

  render() {
    if (
      this.props.name ==
      { data: ["There is no activity in files you uploaded."] }
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
        const byProjectData = this.props.name.data.byProject;
        const columns = [
          {
            Header: "Activity ID",
            accessor: "index",
            id: "index",
            show: false
          },
          {
            Header: "Activity Type",
            accessor: "activityType"
          },
          {
            Header: "From Project",
            accessor: "projectId"
          },
          {
            Header: "Time Appeared",
            accessor: "count",
            filterable: false
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
                data={byProjectData}
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
            Header: "Activity ID",
            accessor: "index",
            show: false
          },
          {
            Header: "Activity Type",
            accessor: "activityType"
          },
          {
            Header: "From Project",
            accessor: "projectId"
          },
          {
            Header: "From File",
            accessor: "filePath"
          },
          {
            Header: "Time Appeared",
            accessor: "count",
            filterable: false
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
