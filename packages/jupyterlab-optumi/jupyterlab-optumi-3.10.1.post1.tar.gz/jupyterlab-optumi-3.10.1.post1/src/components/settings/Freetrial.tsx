/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { DIV, Global, LI, SPAN, UL } from '../../Global';

import { Chip } from '@mui/material';

import FormatUtils from '../../utils/FormatUtils';
import { Header, Label } from '../../core';
import { InfoPopup } from '../../core/InfoPoppup';
import { PlansPopup } from '../../core/PlansPopup';
import { SubscribeButton } from '../../core/SubscribeButton';


// Properties from parent
interface IProps {
    balance: number
}

// Properties for this component
interface IState {
    portalWaiting: boolean,
    showStoragePopup: boolean
    plansOpen: boolean
}

export class FreeTrial extends React.Component<IProps, IState> {
    _isMounted = false;

    constructor(props: IProps) {
        super(props);
        this.state = {
            portalWaiting: false,
            showStoragePopup: false,
            plansOpen: false,
        }
    }

	// The contents of the component
	public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
		return (
            <>
                <DIV sx={{display: 'flex'}}>
                    <Header title='Current plan' />
                    <PlansPopup
                        open={this.state.plansOpen}
                        handleClose={() => this.safeSetState({ plansOpen: false })}
                        openButton={
                            <Chip label='View plans' variant='filled'
                                sx={{
                                    height: '20px',
                                    fontSize: '12px',
                                    marginTop: 'auto',
                                    marginBottom: 'auto',
                                }}
                                onClick={() => this.safeSetState({ plansOpen: true })}
                            />
                        }
                    />
                </DIV>
                <SPAN sx={{display: 'inline-flex'}}>
                    <Label label='Free trial:'
                        getValue={() => FormatUtils.formatCredit(this.props.balance) + ' credit'}
                        align='left' valueAlign='right' labelWidth='164px' lineHeight='12px'
                    />
                    <InfoPopup title='Free Trial' popup={
                        <DIV sx={{padding: '12px'}}>
                                A few things to remember about your free trial:
                            <UL>
                                <LI>No credit card required</LI>
                                <LI>It is valid for 2 weeks</LI>
                                <LI>You get a $5 promotional credit for machines to run notebooks</LI>
                                <LI>At the end of the trial your promotional credit will expire and your data will be deleted (unless you subscribe!)</LI>
                            </UL>
                        </DIV>
                    } sx={{marginLeft: '-6px'}} />
                </SPAN>
                <Label label='Storage:'
                    getValue={() => 'Up to ' + FormatUtils.styleCapacityUnitValue()(Global.user.storageBuckets[0].limit)}
                    align='left' labelWidth='164px' lineHeight='12px'
                />
                <Label label='Egress:'
                    getValue={() => 'Up to ' + FormatUtils.styleCapacityUnitValue()(Global.user.egressBuckets[0].limit)}
                    align='left' labelWidth='164px' lineHeight='12px'
                />
                <DIV sx={{padding: '12px', width: '100%'}}>
                    <SubscribeButton sx={{width: '256px'}}/>
                </DIV>
            </>
		);
    }
    
    // Will be called automatically when the component is mounted
	public componentDidMount = () => {
        this._isMounted = true;
	}

	// Will be called automatically when the component is unmounted
	public componentWillUnmount = () => {
        this._isMounted = false;
    }
    
    private safeSetState = (map: any) => {
		if (this._isMounted) {
			let update = false
			try {
				for (const key of Object.keys(map)) {
					if (JSON.stringify(map[key]) !== JSON.stringify((this.state as any)[key])) {
						update = true
						break
					}
				}
			} catch (error) {
				update = true
			}
			if (update) {
				if (Global.shouldLogOnSafeSetState) console.log('SafeSetState (' + new Date().getSeconds() + ')');
				this.setState(map)
			} else {
				if (Global.shouldLogOnSafeSetState) console.log('SuppressedSetState (' + new Date().getSeconds() + ')');
			}
		}
	}
}
