from rxconfig import config
import reflex as rx
import pymysql
from reflex.components.datadisplay.dataeditor import (
    DataEditorTheme,
)


######################################################################
#############################  Style & DB ###########################
#####################################################################

light_green = '#ECFDF5'
normal_green = '#2BC381'
dark_green = 'rgba(4, 27, 30, 0.7)'

dark_theme = {
    "accent_color": "#044B1E",
    "accent_light": "#021215",
    "text_dark": light_green,
    "text_header": normal_green,
    "text_header_selected": "#000000",
    "bg_cell": "rgba(4, 27, 30, 1)",
    "bg_cell_medium": "#001315",
    "bg_header": "#002d28",
    "bg_header_has_focus": "#143430",
    "bg_header_hovered": "#143430",
    "bg_bubble": "#212121",
    "bg_bubble_selected": "#000000",
    "border_color": "#002d28",
    "header_font_style": "bold 25px",
    "base_font_style": "bold 20px",
}

style = {
    '@keyframes move-it': {
        '0%': {
            'background-position': 'initial'
        },
        '100%': {
            'background-position': '100px 0px'
        }
    },
    'background': 'repeating-linear-gradient(45deg, #041B1E, #041B1E 5%, #001315 5%, #001315 40%)',
    'background-size': '100px 100px',
    'animation': 'move-it 2s linear infinite'

}


def connect_db():
    return pymysql.connect(
        host="sql.freedb.tech",
        user='freedb_osama',
        password="qz!5sxM!YFyaV7V",
        db="freedb_OsamaAbdElMohsenPortofolio",
    )


conn = connect_db()
######################################################################
#############################  Style & DB ###########################
#####################################################################

######################################################################
##############################  Classes  #############################
######################################################################


class State(rx.State):
    """The app state."""


class DataEditorState_HP(rx.State):

    def Get_db_User_info(*args):
        sql = 'SELECT * FROM user_info LIMIT 1'
        conn = connect_db()
        cur = conn.cursor()
        cur.execute(sql)
        data = list(cur.fetchall())
        data = data[0]
        cur.close()
        return data

    user_name: str = ''
    password: str = ''
    logo: str = ''
    pio: str = ''
    user_nametemp: str = ''
    passwordtemp: str = ''
    logotemp: str = ''
    piotemp: str = ''
    (x, user_name, password, logo, pio) = Get_db_User_info()
    (x, user_nametemp, passwordtemp, logotemp, piotemp) = Get_db_User_info()

    cat: str = ' '
    Image_Path: str = ' '
    Header: str = ' '
    Description: str = ' '
    Tags: str = ' '
    newdata: int = 2
    delete_id: int

    clicked_data: str = "Cell clicked: "

    cols: list[str] = [
        {"title": "Id",
         "type": "int",
         "width": 50,
         },
        {
            "title": "Category",
            "type": "str",
        },
        {
            "title": "Image_Url",
            "type": "str",
            "width": 350,
        },
        {
            "title": "Header",
            "type": "str",
        },
        {
            "title": "Description",
            "type": "str",
            "width": 400,
        },
        {
            "title": "Tags",
            "type": "str",
            "width": 300,
        },
    ]

    def refresh_dataB():
        data = []
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("select * from data")
        output = list(cur.fetchall())
        cur.close()
        data += output
        return data

    data: list = refresh_dataB()

    def update_user_info(self):
        self.user_name = self.user_nametemp
        self.password = self.passwordtemp
        self.logo = self.logotemp
        self.pio = self.piotemp
        conn = connect_db()
        cur = conn.cursor()
        sql = "UPDATE user_info SET Username = %s ,password = %s ,logo_icon = %s ,pio = %s WHERE Id = 1"
        value = (self.user_name, self.password, self.logo, self.pio)
        cur.execute(sql, value)
        conn.commit()
        cur.close()
        self.refresh_data()

    def add_data(self):
        if self.cat != ' ' and self.Image_Path != ' ' and self.Header != ' ' and self.Description != ' ' and self.Tags != ' ':
            conn = connect_db()
            cur = conn.cursor()
            sql = "INSERT INTO data (Category, Image_Path, Header, Description, Tags) VALUES (%s, %s, %s, %s, %s)"
            value = (self.cat, self.Image_Path, self.Header,
                    self.Description, self.Tags)
            cur.execute(sql, value)
            conn.commit()
            cur.close()
            self.refresh_data()

    def click_cell(self, pos):
        col, row = pos
        self.data = []
        self.refresh_data()

    def get_edited_data(self, pos, val) -> str:
        col, row = pos
        # self.data[row][col] = val["data"]
        # print("self.data[row][col] = ", self.data[row][col])
        # print(f"Id {self.data[row][0]} Edited")
        # print(f"current data =  {self.data[row][col]} ")
        # print("new value = ", val['data'])

        conn = connect_db()
        cur = conn.cursor()
        if col == 1:
            sql = "UPDATE data SET Category = %s WHERE Id = %s"
            state = True
        elif col == 2:
            sql = "UPDATE data SET  Image_Path = %s WHERE Id = %s"
            state = True
        elif col == 3:
            sql = "UPDATE data SET  Header = %s WHERE Id = %s"
            state = True
        elif col == 4:
            sql = "UPDATE data SET  Description = %s WHERE Id = %s"
            state = True
        elif col == 5:
            sql = "UPDATE data SET  Tags = %s WHERE Id = %s"
            state = True
        else:
            state = False
            pass

        if state:
            value = (val['data'], self.data[row][0])
            cur.execute(sql, value)
            conn.commit()
            cur.close()
            self.refresh_data()

    def refresh_data(self):
        (self.x, self.user_name, self.password, self.logo, self.pio) = self.Get_db_User_info()
        print('='*100)
        print('user_info = ')
        print((self.x, self.user_name, self.password, self.logo, self.pio))        
        print('='*100)
        self.data = []
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("select * from data")
        output = list(cur.fetchall())
        cur.close()
        self.data += output
        print('='*100)
        print('self.data = ')
        print(self.data)
        print('='*100)
        print('output = ')
        print(output)

    def set_delete_id(self, text: str):
        try:
            self.delete_id = int(text)
        except:
            pass

    def delete_data(self):
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute(f"DELETE FROM data WHERE Id = {self.delete_id}")
            conn.commit()
            cur.close()
            self.refresh_data()
        except:
            pass


class CardSwitcherState(rx.State):
    current_card_index: int = 0
    names = ["Python", "C", "HTML"]
    progr = ['100', '20', '30']
    image = ['/Netflix_Dashboard_tableau.png', '/01.png', '/02.png']

    def next_card(self):
        if self.current_card_index < len(self.names) - 1:
            self.current_card_index += 1

    def previous_card(self):
        if self.current_card_index > 0:
            self.current_card_index -= 1


class Portal_password(rx.State):
    pin: str
    state: int = 2

    def Check_password(self):
        db_password = Get_db_password()
        if db_password == self.pin:
            self.state = 1
        else:
            self.state = 0


######################################################################
##############################  Classes  #############################
######################################################################


######################################################################
###############################  BARS  ###############################
######################################################################

def navbar():
    """The navbar for the top of the page."""
    return rx.chakra.box(
        rx.chakra.hstack(
            rx.chakra.hstack(
                rx.chakra.image(src=DataEditorState_HP.logo, width="50px"),
                rx.heading(DataEditorState_HP.user_name),
            ),
            justify="space-between",
            padding_x="2em",
            padding_y="1em",
            box_shadow="lg",
        ),
        background_color="rgba(4, 27, 30, 0.7)",
        panel_background='translucent',
        position="fixed",
        width="100%",
        top="0px",
        z_index="500",
    )

def bottombar():
    return rx.flex(
        rx.hstack(
            rx.text(
                "© 2024 Developed and Designed With 💖 by : ".upper(),
                size='5',
                font_family="Vobca-Black",
                color=light_green,
            ),
            rx.text(
                "Osama Abd El Mohsen".upper(),
                size='5',
                font_family="Vobca-Black",
                color=normal_green,
            ),
            align="center",
            justify="center",
            padding="2px",
        ),
        align="center",
        justify="center",
        position="fixed",
        bottom="0",
        width="100%",
        padding="2px",
        background_color='rgba(4, 27, 30, 1)',
        z_index="500",
        color=light_green,
    )

######################################################################
###############################  BARS  ###############################
######################################################################


def skill(skillName, precentage, image):
    return rx.card(
        rx.inset(
            rx.center(
                rx.image(
                    src=image,
                    width="auto",
                    height="500px",
                ),
            ),
            side="top",
            pb="current",
            background_color="rgba(36, 36, 36, 1)",
        ),
        rx.heading(
            "Reflex is a web framework that allows developers to build their app in pure Python."
        ),
        rx.divider(),
        rx.heading(
            "Reflex is a web framework that allows developers to build their app in pure Python."
        ),
        rx.divider(),
        rx.heading(
            f"Skill name = {skillName}"
        ),
        rx.divider(),
        rx.progress(
            value=int(precentage),
            max=100
        ),
        rx.divider(),
        spacing='10',
    )


######################################################################
############################  Helper Func  ###########################
######################################################################
def letter_heading(char):
    return rx.center(
        rx.chakra.text(char, font_size="2em", font_family="Hackonedash", color=light_green,text_shadow=f"0 0 5px {normal_green}"),
        )


def Get_db_password():
    sql = 'SELECT password FROM user_info LIMIT 1'
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(sql)
    output = list(cur.fetchall())
    output = str(output[0])
    output = output[output.index("'")+1:-3]
    cur.close()
    return output


def password_ui():
    return rx.chakra.vstack(
        rx.chakra.heading(Portal_password.pin),
        rx.chakra.box(
            rx.chakra.pin_input(
                length=8,
                on_change=Portal_password.set_pin,
                on_complete=Portal_password.Check_password(),
                mask=True,
                shadow="md",
                color=normal_green
            ),
        ),
    )

######################################################################
############################  Helper Func  ###########################
######################################################################

######################################################################
###############################  Pages  ##############################
######################################################################


def index() -> rx.Component:
    DataEditorState_HP.refresh_data()
    return rx.chakra.center(
        rx.chakra.vstack(
            navbar(),
            bottombar(),
            rx.image(
                src="https://readme-typing-svg.herokuapp.com/?lines=Mechatronics%20Engineer;Always%20learning%20new%20things&font=Fira%20Code&center=true&width=440&height=45&color=3DB54A&vCenter=true&size=22"
            ),
            rx.flex(
                rx.heading(
                    rx.code_block(
                        'print("Hello ...  Iam Osama Abd EL Mohsen From Egypt a final year undergraduatefrom Mansoura University")',
                        language="python",
                        show_line_numbers=False,
                        wrap_long_lines=True,),  size='5'
                ),
                rx.chakra.card(
                    rx.hstack(
                        rx.flex(
                            rx.flex(
                                rx.foreach(list('Data'.upper()), letter_heading),
                                direction="column",
                                size="3xl"
                            ),
                            rx.flex(
                                rx.foreach(list('Analysis'.upper()), letter_heading),
                                direction="column",
                                size="3xl"
                            ),
                            spacing="3",
                            direction="row",
                            width='10%',

                        ),
                        rx.flex(
                            rx.icon(
                                tag="chevron-left",
                                size=90,
                                on_click=CardSwitcherState.previous_card,
                                _hover={"color": "var(--green-11)"},
                                _active={
                                    "color": "var(--green-9)"},
                            ),
                            skill(
                                CardSwitcherState.names[CardSwitcherState.current_card_index], '50', CardSwitcherState.image[CardSwitcherState.current_card_index]),
                            rx.icon(
                                tag="chevron-right",
                                size=90,
                                on_click=CardSwitcherState.next_card,
                                _hover={"color": "var(--green-11)"},
                                _active={
                                    "color": "var(--green-9)"},
                            ),
                            align="center",
                            spacing='3',
                        ),
                    ),
                    font_size="2em",
                    font_family="MyFont",
                ),
                rx.chakra.card(
                    rx.hstack(
                        rx.flex(
                            rx.icon(
                                tag="chevron-left",
                                size=90,
                                on_click=CardSwitcherState.previous_card,
                                _hover={"color": "var(--green-11)"},
                                _active={
                                    "color": "var(--green-9)"},
                            ),
                            skill(
                                CardSwitcherState.names[CardSwitcherState.current_card_index], '50', CardSwitcherState.image[CardSwitcherState.current_card_index]),
                            rx.icon(
                                tag="chevron-right",
                                size=90,
                                on_click=CardSwitcherState.next_card,
                                _hover={"color": "var(--green-11)"},
                                _active={
                                    "color": "var(--green-9)"},
                            ),
                            align="center",
                            spacing='3',
                        ),
                        rx.flex(
                            rx.foreach(list('Python'.upper()), letter_heading),
                            direction="column",
                            spacing="3",
                            width='10%',
                            size="3xl",

                        ),
                    ),
                    font_size="2em",
                ),
                variant='ghost',
                spacing="3",
                direction="column",
            ),
        ),
        padding="5em"
    )


def portal_true():
    DataEditorState_HP.refresh_data()
    return rx.chakra.center(
        rx.chakra.vstack(
            navbar(),
            bottombar(),
            rx.chakra.spacer(),
            rx.chakra.spacer(),
            rx.chakra.spacer(),
            rx.chakra.spacer(),
            rx.hstack(
                rx.flex(
                    rx.card(
                        rx.card(
                            rx.flex(
                                rx.chakra.text(
                                    'Update User Info'.upper(), color=normal_green,font_family="Hackonedash",font_size='3em'),
                                spacing='4',
                                direction='row',
                            ),
                            variant='ghost'
                        ),
                        rx.card(
                            rx.flex(
                                rx.chakra.input(
                                    focus_border_color=normal_green, placeholder='User Name', value=DataEditorState_HP.user_name, on_change=DataEditorState_HP.set_user_nametemp),
                                rx.chakra.input(
                                    focus_border_color=normal_green, type_="password", max_length="8", placeholder='Password', value=DataEditorState_HP.password, on_change=DataEditorState_HP.set_passwordtemp),
                                spacing='4',
                                direction='row',
                            ),
                            variant='ghost'
                        ),
                        rx.card(
                            rx.flex(
                                rx.chakra.text_area(
                                    focus_border_color=normal_green, placeholder='pio', font_size="1em", width='100%', value=DataEditorState_HP.pio, on_change=DataEditorState_HP.set_piotemp),
                                spacing='4',
                                direction='row',
                            ),
                            variant='ghost'
                        ),
                        rx.card(
                            rx.flex(
                                rx.chakra.input(
                                    focus_border_color=normal_green, placeholder='Icon url', value=DataEditorState_HP.logo, on_change=DataEditorState_HP.set_logotemp),
                                rx.chakra.button(rx.icon(tag="save", stroke_width=2.5), "Update",on_click=DataEditorState_HP.update_user_info, width='100%', bg=dark_green, color=light_green, spacing="10"),
                                spacing='4',
                                direction='row',
                            ),
                            variant='ghost'
                        ),
                        variant='ghost'
                    ),
                    rx.chakra.spacer(),
                    rx.chakra.spacer(),
                    rx.chakra.spacer(),
                    rx.chakra.center(
                        rx.chakra.divider(border_color=normal_green,orientation="vertical"),
                        height="20em",
                        align = 'center'
                    ),
                    rx.chakra.spacer(),
                    rx.chakra.spacer(),
                    rx.chakra.spacer(),
                            rx.card(
                        rx.card(
                            rx.flex(
                                rx.chakra.text(
                                    'Update Data '.upper(), color=normal_green,font_family="Hackonedash",font_size='3em'),
                                spacing='4',
                                direction='row',
                            ),
                            variant='ghost'
                        ),
                        rx.card(
                            rx.flex(
                                rx.chakra.input(
                                    focus_border_color=normal_green, placeholder="Category", on_blur=DataEditorState_HP.set_cat),
                                rx.chakra.input(
                                    focus_border_color=normal_green, placeholder="Image_Path", on_blur=DataEditorState_HP.set_Image_Path),
                                spacing='4',
                                direction='row',
                            ),
                            variant='ghost'
                        ),
                        rx.card(
                            rx.flex(
                                rx.chakra.input(
                                    focus_border_color=normal_green, placeholder="Header", on_blur=DataEditorState_HP.set_Header),
                                rx.chakra.input(
                                    focus_border_color=normal_green, placeholder="Description", on_blur=DataEditorState_HP.set_Description),
                                spacing='4',
                                direction='row',
                            ),
                            variant='ghost',
                        ),
                        rx.card(
                            rx.flex(
                                rx.chakra.input(
                                    focus_border_color=normal_green, placeholder="Tags", on_blur=DataEditorState_HP.set_Tags),
                                rx.chakra.button(rx.icon(tag="plus", stroke_width=2.5), "Add", on_click=DataEditorState_HP.add_data,width='100%', bg=dark_green, color=light_green, spacing="10"),
                                spacing='4',
                                direction='row',
                            ),
                            variant='ghost',
                        ),
                        variant='ghost',
                        direction='row',
                    ),
                    variant='ghost',
                    spacing='4',
                    direction='row',
                )
            ),
            rx.chakra.spacer(),
            rx.chakra.spacer(),
            rx.chakra.divider(border_color=normal_green),
            rx.chakra.spacer(),
            rx.chakra.spacer(),
            rx.flex(
                rx.chakra.button(rx.icon(tag="refresh-ccw", stroke_width=2.5), "Refresh Data",
                                 on_click=DataEditorState_HP.refresh_data, bg="#0C4466", color="#D2EAFC", width="100%", spacing="10"),
                rx.chakra.input(focus_border_color=normal_green, placeholder="Delete",
                                on_blur=DataEditorState_HP.set_delete_id, width="100%"),
                rx.chakra.button(rx.icon(tag="trash", stroke_width=2.5), "Delete",
                                 on_click=DataEditorState_HP.delete_data, width="100%", bg="#681212", color="#fef2f2", spacing="10"),
                spacing='4',
                direction='row'
            ),
            rx.chakra.spacer(),
            rx.chakra.spacer(),
            rx.chakra.divider(border_color=normal_green),
            rx.hstack(
                rx.data_editor(
                    columns=DataEditorState_HP.cols,
                    data=DataEditorState_HP.data,
                    on_cell_edited=DataEditorState_HP.get_edited_data,
                    row_height=80,  # Adjusting row height for better readability
                    font_size="5em",
                    theme=DataEditorTheme(**dark_theme),
                    fixed_shadow_x=False,
                    fixed_shadow_y=False,
                    column_select='none'


                ),

            ),
        ),
        padding="5em"
    )


def portal_wrong():
    return rx.chakra.center(
        rx.chakra.vstack(
            navbar(),
            rx.heading("Enter Your Portal Pin",
                       font_family="Azonix", color=light_green),
            password_ui(),
            bottombar(),
        ),
        padding="5em"
    )


def portal():
    return rx.center(
        rx.vstack(
            rx.cond(
                Portal_password.state == 1,
                portal_true(),
                portal_wrong(),
            ),
            rx.cond(
                Portal_password.state == 0,
                rx.heading("Wrong password", color='#b91c1c',
                           font_family="Azonix",),
                rx.heading(' '),
            ),
            align='center'
        )
    )
######################################################################
###############################  Pages  ##############################
######################################################################


######################################################################
###############################   App   ##############################
######################################################################
app = rx.App(
    style=style,
    stylesheets=[
        "/fonts/myfont.css",
    ],
    theme=rx.theme(
        appearance="dark",
        has_background=True,
        accent_color="green",
        grayColor="mauve",
        panel_background='translucent',
        radius="large",
    )
)
app.add_page(index)
app.add_page(portal, route="/portal")
######################################################################
###############################   App   ##############################
######################################################################
