import streamlit as st
from streamlit_sortables import sort_items
from streamlit_server_state import server_state, server_state_lock
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

if 'flag' not in server_state:
    server_state.flag = False
if 'dat' not in server_state:
    server_state.dat = [
    {'header':'Loops','items':['Outer']},
    {'items':['Inner']},
    {'header':'Extra rows','items':['----','2201','2202','2203','2204','2205']},
    {'items':['----','2701','2861','2702','2707','4701','4704','4711','4715',]},
    {'items':['----','2307','2321','2328','2706']},
    {'items':['----','2206','2207','2208','2209','2210','2211','2212']},
    {'items':['----','4720','5702','5703','5715','5905']}
    ]
if 'dat2' not in server_state:
    server_state.dat2 = server_state.dat.copy()
if 'show_dd' not in st.session_state:
    st.session_state.show_dd = False

st.subheader("Bus Loop View")
st.image('https://github.com/banananana6/phsbuses/blob/deee3a87f707aca562977a4019fa4b9dfe85698e/assets/img/beyond_phs.png?raw=true')

items1 = server_state.dat2[0]['items']
cols = st.columns(max(8,len(items1)))
if (len(items1)<=8):
    for i, item in enumerate(items1):
        if i>0:
            with cols[i+8-len(items1)]:
                st.button(item, key=f"sorted3_{i}")
else:
    for i, item in enumerate(items1):
        if i>0:
            with cols[i]:
                st.button(item, key=f"sorted3_{i}")

items2 = server_state.dat2[1]['items']
cols = st.columns(max(8,len(items2)))
if (len(items2)<=8):
    for i, item in enumerate(items2):
        if i>0:
            with cols[i+8-len(items2)]:
                st.button(item, key=f"sorted4_{i}")
else:
    for i, item in enumerate(items2):
        if i>0:
            with cols[i]:
                st.button(item, key=f"sorted4_{i}")
st.image('https://github.com/banananana6/phsbuses/blob/deee3a87f707aca562977a4019fa4b9dfe85698e/assets/img/phs_building.png?raw=true')

name, authentication_status, username = authenticator.login(fields={'Form name':'Login', 'Username':'Username', 'Password':'Password','Login':'Login'})
print(st.session_state["authentication_status"])
print(st.session_state["username"])
if st.session_state["authentication_status"]:
    with st.container(border=True):
        st.subheader('Logout')
        st.checkbox('Verify logout', key='verify_logout')
    if st.session_state.verify_logout:
        authenticator.logout()
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.title('Admin: Bus drag-and-drop')

    with st.form("my_form"):
        st.write("Add, change, or remove sub-bus number")
        orig_num = st.text_input("Regular Bus Number", "")
        sub_num = st.text_input("Sub-Bus Number", "")
        if st.form_submit_button('Submit'):
            if orig_num == '':
                st.warning("Please enter the original bus number")
            else:
                row_flag = False
                for row in range(6):
                    for i in range(len(server_state.dat[row]['items'])):
                        if (server_state.dat[row]['items'][i][0:4]==orig_num):
                            if sub_num=='':
                                server_state.dat[row]['items'][i] = str(orig_num)
                            else:
                                server_state.dat[row]['items'][i] = str(orig_num)+"\n ("+str(sub_num)+")" 
                            row_flag=True
                if row_flag==False:
                    st.warning("Please enter a valid original bus number")

    st.subheader("Drag-and-drop")
    if (st.button("Reset drag and drop")):
        server_state.dat = [
    {'header':'Loops','items':['Outer']},
    {'items':['Inner']},
    {'header':'Extra rows','items':['----','2201','2202','2203','2204','2205']},
    {'items':['----','2701','2861','2702','2707','4701','4704','4711','4715',]},
    {'items':['----','2307','2321','2328','2706']},
    {'items':['----','2206','2207','2208','2209','2210','2211','2212']},
    {'items':['----','4720','5702','5703','5715','5905']}
        ]
        server_state.dat2 = [
    {'header':'Loops','items':['Outer']},
    {'items':['Inner']},
    {'header':'Extra rows','items':['----','2201','2202','2203','2204','2205']},
    {'items':['----','2701','2861','2702','2707','4701','4704','4711','4715',]},
    {'items':['----','2307','2321','2328','2706']},
    {'items':['----','2206','2207','2208','2209','2210','2211','2212']},
    {'items':['----','4720','5702','5703','5715','5905']}
        ]
    if st.button('Show drag-and-drop' if not st.session_state.show_dd else 'Hide drag-and-drop'):
        st.session_state.show_dd = not st.session_state.show_dd
    if st.session_state.show_dd:
        sorted = sort_items(server_state.dat, multi_containers=True)
        server_state.dat = sorted.copy()

    server_state.dat2 = server_state.dat.copy()

    data = server_state.dat

elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('For admins only: please enter your username and password')
