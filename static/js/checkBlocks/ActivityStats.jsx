import React from "react";
import ReactTable from "react-table";
import "react-table/react-table.css";
import Enumerable from "linq";

export default class ActivityStatsBlock extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      actText: "All Activities",
      fileText: "All Files",
      projectText: "All Projects"
    };
  }
  render() {
    var data = JSON.parse(this.props.name.replace(/'/g, '"'));
    var activity = data.activity;
    var file = data.file;
    var project = data.project;
    data = data.data;

    if (this.state.actText != "All Activities") {
      data = data.filter(d => {
        return d.activityType.match(this.state.actText);
      });
    }
    if (this.state.fileText != "All Files") {
      data = data.filter(d => {
        return d.file.match(this.state.fileText);
      });
    }
    if (this.state.projectText != "All Projects") {
      data = data.filter(d => {
        return d.project.match(this.state.projectText);
      });
    }

    var query = Enumerable.from(data)
      .groupBy(
        "{activityType: $.activityType, project: $.project }",
        "parseInt($.count) | 0",
        "{activityType: $.activityType, project: $.project, count: parseInt($$.sum()) }",
        "$.activityType + ' ' + $.project"
      )
      .toArray();
    for (var i = 0; i < query.length; i++) {
      query[i].index = i + 1;
    }
    const columns = [
      {
        Header: "id",
        accessor: "index",
        id: "index",
        show: false
      },
      {
        Header: "Activity Type",
        accessor: "activityType"
      },
      {
        Header: "Project",
        accessor: "project"
      },
      {
        Header: "Time Used",
        accessor: "count"
      }
    ];
    return (
      <React.Fragment>
        <div className="row justify-content-lg-left">
          <div className="col-lg-12">
            <div className="ml-4 mt-4 mb-4">
              <span className="heading-1 d-block">Activity Statistics</span>
              <span className="heading-2 mb-3 d-block">
                Here is a summary of how many times each activities is used in
                the uploaded files.
              </span>
            </div>
            <div className="ml-3 mt-4 mb-4" id="actFilters">
              <div className="dropdown d-inline ml-2">
                <button
                  className="btn btn-primary extra-button-styles dropdown-toggle"
                  style={{ verticalalign: "top" }}
                  type="button"
                  data-toggle="dropdown"
                  aria-haspopup="true"
                  aria-expanded="false"
                  id="actTypeFilter"
                >
                  {this.state.actText}
                </button>

                <div
                  className="dropdown-menu"
                  aria-labelledby="dropdownMenu2"
                  id="actTypeDropdownMenu"
                >
                  {activity.map(act => (
                    <li
                      className="dropdown-item"
                      key={"acttype" + act.index}
                      onClick={() =>
                        this.setState({ actText: event.target.innerText })
                      }
                    >
                      {act.activityType}
                    </li>
                  ))}
                </div>
              </div>
              <div className="dropdown d-inline ml-3">
                <button
                  className="btn btn-primary extra-button-styles dropdown-toggle"
                  style={{ verticalalign: "top" }}
                  type="button"
                  data-toggle="dropdown"
                  aria-haspopup="true"
                  aria-expanded="false"
                  id="actFileFilter"
                >
                  {this.state.fileText}
                </button>

                <div
                  className="dropdown-menu"
                  aria-labelledby="dropdownMenu2"
                  id="fileDropdownMenu"
                >
                  {file.map(f => (
                    <li
                      className="dropdown-item"
                      key={"actfile" + f.index}
                      onClick={() =>
                        this.setState({ fileText: event.target.innerText })
                      }
                    >
                      {f.file}
                    </li>
                  ))}
                </div>
              </div>
              <div className="dropdown d-inline ml-3">
                <button
                  className="btn btn-primary extra-button-styles dropdown-toggle"
                  style={{ verticalalign: "top" }}
                  type="button"
                  id="dropdownMenu2"
                  data-toggle="dropdown"
                  aria-haspopup="true"
                  aria-expanded="false"
                  id="actProjectFilter"
                >
                  {this.state.projectText}
                </button>
                <div className="dropdown-menu" aria-labelledby="dropdownMenu2">
                  {project.map(p => (
                    <li
                      className="dropdown-item"
                      key={"t1project" + p.index}
                      onClick={() =>
                        this.setState({ projectText: event.target.innerText })
                      }
                    >
                      {p.project}
                    </li>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="row">
          <div className="col-lg-12">
            <div className="col-lg-12">
              <ReactTable
                className="table table_fixed ml-2 mr-2"
                columns={columns}
                data={query}
                defaultPageSize={10}
                showPageSizeOptions={false}
                defaultSorted={[
                  {
                    id: "count",
                    desc: true
                  },
                  {
                    id: "project",
                    desc: false
                  },
                  {
                    id: "activityType",
                    desc: false
                  }
                ]}
              />
            </div>
          </div>
        </div>
      </React.Fragment>
    );
  }
}
