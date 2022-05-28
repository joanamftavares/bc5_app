import streamlit as st

def app():
    st.title('Home')

    st.write('Investments4Some is a long-standing Portuguese, privately-held hedge funds management firm. We have been exploring Machine Learning models for market price forecasting, which we use to anticipate market trends. This App was thought as a tool to help you take better decisions regarding investments, improve the quality of your portfolios and provide an easy way to keep track of the market trends.')
    #st.image('APPS//logo.png')
    col1, col2 = st.columns(2)

    with col1:
        st.image('apps//logo.png')
        st.write("#### **How long have you been investing?**")
        if st.checkbox('I just started investing'):
            expander = st.expander("Here are few tips for you")
            expander.write("""
            The most important steps to undertake for a new investor are the establishment of a plan and understand important concepts such as risk, diversity and include these in your investment plan as well as your reinvestment strategy. Investing involves risks and every investor must be aware of it before starting this journey. 
There are a few questions to consider when establishing your plan:
* How much can you invest? 
* How much can you afford to lose?  
* What is the primary objective of your investments? 
* How long are you investing for to reach that goal? 
* Are you aware of the investment’s terminology?
Other aspects should also be regarded, especially if you are investing in a high volatile market. Do you prefer to invest a large amount at once or invest regularly? For example, when investing in a volatile market, Pound Cost Averaging could be beneficial because by investing with regularity, you can balance the highs and lows of the market.
If you are interested in investing in the cryptocurrency market, be careful and look for reliable specialists. Be aware that cryptocurrency trading is a high-risk business, and you should not invest more money than you can afford to lose. Moreover, try to diversify your money among different cryptos, which decreases the risk of being harmed if there is a crash in one of the digital currencies.
             """)
        op2 = st.checkbox('I have been investing for a while')


    with col2:#escrever tips
        st.markdown('### **Select one per category:**')
        count = 0
        st.write('#### **How do you feel about risk?**')
        if st.checkbox('I prefer low risk investments'):
            count = count+ 1
        if st.checkbox('I dont have a preference of risk'):
            count = count + 2
        if st.checkbox('I prefer high risk investments'):
            count = count + 3

        st.write("#### **What about return of investments?**")
        if st.checkbox('I dont mind having a low return of investments'):
            count = count + 1
        if st.checkbox('I dont mind having a moderate return of investments'):
            count = count + 2
        if st.checkbox('I want a high return of investments'):
            count = count + 3

        st.write("#### **Are you in a rush to access your funds?**")
        if st.checkbox('I want to access my funds as soon as possible'):
            count = count + 1
        if st.checkbox('I want to access my funds in a medium period of time'):
            count = count + 2
        if st.checkbox('I dont mind waiting to access my funds'):
            count = count + 3

        if (count ==0):
            st.markdown(f'<b><p style="background-color:#FFEC4F;color:#000000;font-size:24px;border-radius:3%;text-align:center;">What type of investor are you? Take the quizz!</p></b>', unsafe_allow_html=True)
        elif (count <=4):
            st.markdown(f'<b><p style="background-color:#FFEC4F;color:#000000;font-size:24px;border-radius:3%;text-align:center;">Conservative Investor</p></b>',unsafe_allow_html=True)
        elif ((count>=5) & (count <=7)):
            st.markdown(f'<b><p style="background-color:#FFEC4F;color:#000000;font-size:24px;border-radius:3%;text-align:center;">Moderate Investor</p></b>',unsafe_allow_html=True)
        else:
            st.markdown(f'<b><p style="background-color:#FFEC4F;color:#000000;font-size:24px;border-radius:3%;text-align:center;"> Bold Investor</p></b>',unsafe_allow_html=True)

