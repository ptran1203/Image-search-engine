import React from 'react';
import { BasePage } from '../BaseComponent/BasePage.jsx';
import $ from 'jquery';
import NavBar from '../reactComponents/general/NavBar.jsx';

class Layout extends BasePage {
    constructor(props) {
        super(props);

        this.state = {
            tabIndex: 0
        }
        console.log(this.state);
    }

    renderBody() {
        throw new Error("not implemented exception!");
    };
    _onClickHome = () => {
        this.setState({tabIndex: 0});
    }
    _onClickNoti = () => {
        this.setState({tabIndex: 1});
    }
    _onClickProfile = () => {
        this.setState({tabIndex: 2});
    }
    _onClickAbout = () => {
        this.setState({tabIndex: 3});
    }
    childrenRender = () => {
        let { classes, ...rest } = this.props;

        return (
            <React.Fragment>
                <div className="body-layout">
                    {this.renderBody()}
                </div>
                <NavBar 
                    onClickHome={this._onClickHome}
                    onClickNoti={this._onClickNoti}
                    notiCount={3}
                    onClickProfile={this._onClickProfile}
                    onClickAbout={this._onClickAbout}
                    currentTab={this.state.tabIndex}
                />
            </React.Fragment>
        );
    };
}



export default Layout;

