import React from 'react';

const Result = props => {
    let { data } = props;
    var rows = data.chunk_(4);
    return (
        <React.Fragment>
            {/* {data.map((i, index) => {

                return (
                    <div key={index + "col"} className="col-md-3 col-sm-3">
                        <div style={{ width: '100%' }}>
                            <img src={i.path} style={{ width: '100%' }} />
                            <p>{i.accuracy}</p>
                        </div>
                    </div>
                )
            })} */}
            <h3>Kết quả</h3>
            {data && rows.map((row, rindex) => {
                return (
                    <div className="row" key={rindex + "row"}>
                        {row.map((i, index) => {
                            return (
                                <div key={index + "col"} className="col-md-3 col-sm-3">
                                    <div style={{ width: '100%' }}>
                                        <img src={i.path} style={{ width: '100%' }} />
                                        <p>{i.accuracy}</p>
                                    </div>
                                </div>
                            )
                        })}
                    </div>
                )
            })}
        </React.Fragment>
    )
}

export default Result;