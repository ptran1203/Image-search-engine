
import React from 'react';
import { withStyles } from '@material-ui/core';
import Card from "components/Card/Card.jsx";
import CardBody from "components/Card/CardBody.jsx";
import GridContainer from 'components/Grid/GridContainer.jsx';
import GridItem from 'components/Grid/GridItem.jsx';
class MainAction extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        let {classes, onClickOrder, onClickHistory, className} = this.props;
        let {mainBtn} = classes;
        return (
            <Card className={className} style={{ padding: '0', width: 'auto', marginTop: '15px' }}>
                <CardBody style={{ padding: '0' }}>
                    <GridContainer>
                        <GridItem xs={6}>
                            <div onClick={onClickOrder} className={mainBtn}>
                                <p style={{ color: '#00b6f0' }}>
                                    <i className="fas fa-truck"></i>
                                </p>
                                <p>Đặt giặt</p>
                            </div>
                        </GridItem>
                        <GridItem xs={6}>
                            <div onClick={onClickHistory} className={mainBtn}>
                                <p style={{ color: '#4d2f91' }}>
                                    <i className="fas fa-history"></i>
                                </p>
                                <p>Lịch sử</p>
                            </div>
                        </GridItem>
                    </GridContainer>
                </CardBody>
            </Card>
        )
    }

}
const styles = {
	mainBtn: {
		// border: '1px solid #ccc',
		borderRadius: '5px',
		'& p': {
			textAlign: 'center',
			color: '0a0a0a',
			fontWeight: '500',
            fontSize: '1.2rem 1rem 1rem',
            margin: '0'
		},
		'& i': {
			textAlign: 'center',
			fontSize: '2rem',
		},
        padding: '1rem',
        
	}
}
export default withStyles(styles)(MainAction);