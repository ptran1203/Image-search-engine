
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import SwipeableViews from 'react-swipeable-views';
import React, { Fragment } from 'react';

export default class Swipe extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            index: 0
        }
    }
    handleChange = (e, v) => {
        this.setState({ index: v });
    }
    handleChangeIndex = index => {
        this.setState({ index: index });
    }
    render() {
        let { index } = this.state;
        let { tabs, tabStyles, children } = this.props;
        console.log(children);
        return (
            <Fragment>
                {!tabs ? null :
                    <Tabs
                        value={index}
                        fullWidth onChange={this.handleChange}
                        style={{ ...tabStyles }}
                        TabIndicatorProps={{
                            classes: {
                                root: {
                                    backgroundColor: 'black'
                                }
                            }
                        }}
                    >
                        {tabs.map((tab, index) => {
                            let { label, onClick, styles } = tab;
                            return (
                                <Tab
                                    style={{ ...styles }}
                                    key={`tab-i3-${index}`}
                                    label={label}
                                    onClick={() => { typeof onClick === 'function' && onClick() }}
                                />
                            )
                        })}
                    </Tabs>
                }
                <SwipeableViews
                    enableMouseEvents
                    index={index}
                    onChangeIndex={this.handleChangeIndex}
                >
                    {!children.length ? children : children.map((i, index) => {
                        return (i);
                    })}
                </SwipeableViews>
            </Fragment>
        )
    }

}