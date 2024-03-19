import React, { useEffect } from 'react';
import ReactDOM from 'react-dom';
import { PayPalButtons, usePayPalScriptReducer } from "@paypal/react-paypal-js";
import { BsConeStriped } from 'react-icons/bs';

const PaypalButton = ({ createOrder, onApprove }) => {
    // const PayPalButton = paypal.Buttons.driver("react", { React, ReactDOM });
    const [{ isPending }] = usePayPalScriptReducer();
    const paypal = React.useRef();

    useEffect(() => {
        if (!paypal.current) {
            window.paypal.Buttons({
                createOrder: (data, actions) => {
                    return actions.order
                        .create({
                            intent: "CAPTURE",
                            application_context: {
                                shipping_preference: "NO_SHIPPING",
                                user_action: "PAY_NOW",
                                return_url: "https://localhost:3000/",
                            },
                            purchase_units: [
                                {
                                    amount: {
                                        value: "50.0",
                                        // currency_code: "USD",
                                    },
                                    description: "This is the payment description.",
                                },
                            ],
                        })

                },
                onApprove: async (data, actions) => {
                    const order = await actions.order.capture();
                    console.log(order)
                    // onApprove(order)    
                },
                onError: (err) => {
                    console.log(err)
                }
            }).render(paypal.current)
        }
    }, [])

    return (
        <div>
            (!paypal.current ? <div className="spinner" /> : <div ref={paypal}></div>)
        </div>
        // (isPending ? <div className="spinner" /> : <PayPalButtons
        //     createOrder={createOrder}
        //     onApprove={onApprove}
        //     onInit={(data) => console.log("init", data)}


        // />)

    )
}

export default PaypalButton