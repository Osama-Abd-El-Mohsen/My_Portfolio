from rxconfig import config
import reflex as rx
import pymysql

conn = pymysql.connect(
    host="sql.freedb.tech",
    user='freedb_osama',
    password="qz!5sxM!YFyaV7V",
    db="freedb_OsamaAbdElMohsenPortofolio",
)

# cur = conn.cursor()
# cur.execute("select * from data")
# output = cur.fetchall()


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


class State(rx.State):
    """The app state."""


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


def navbar():
    """The navbar for the top of the page."""
    return rx.chakra.box(
        rx.chakra.hstack(
            rx.chakra.hstack(
                rx.chakra.image(src="/favicon.ico", width="50px"),
                rx.heading("Osama Abd El Mohsen"),
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


def letter_heading(char):
    return rx.chakra.heading(char, font_size="2em", font_family="JetBrainsMono")


def index() -> rx.Component:
    return rx.chakra.center(
        rx.chakra.vstack(
            navbar(),
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
                                rx.foreach(list('Data'), letter_heading),
                                direction="column",
                                size="3xl"
                            ),
                            rx.flex(
                                rx.foreach(list('Analysis'), letter_heading),
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
                            rx.foreach(list('Python'), letter_heading),
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


class InputBlurState(rx.State):

    cat: str = ' '
    Image_Path: str = ' '
    Header: str = ' '
    Description: str = ' '
    Tags: str = ' '
    newdata : int = 2

    def add_data(self):
        if self.cat != ' ' and self.Image_Path != ' ' and self.Header != ' ' and self.Description != ' ' and self.Tags != ' ':
            cur = conn.cursor()
            sql = "INSERT INTO data (Category, Image_Path, Header, Description, Tags) VALUES (%s, %s, %s, %s, %s)"
            value = (self.cat, self.Image_Path, self.Header,self.Description, self.Tags)
            cur.execute(sql, value)
            conn.commit()

    

def Data() -> rx.Component:

    cur = conn.cursor()
    cur.execute("select * from data")
    output = cur.fetchall()
    rows = list(output)

    return rx.chakra.center(
        rx.chakra.vstack(
            navbar(),
            rx.hstack(
                rx.chakra.input(
                    placeholder="Category", on_blur=InputBlurState.set_cat),
                rx.chakra.input(
                    placeholder="Image_Path", on_blur=InputBlurState.set_Image_Path),
                rx.chakra.input(
                    placeholder="Header", on_blur=InputBlurState.set_Header),
                rx.chakra.input(placeholder="Description",
                                on_blur=InputBlurState.set_Description),
                rx.chakra.input(
                    placeholder="Tags", on_blur=InputBlurState.set_Tags),
                rx.chakra.button("Add", on_click=InputBlurState.add_data),
                
            ),
            rx.chakra.table_container(
                rx.chakra.table(
                    headers=["Id", "Category", "Image_Path",'Header', 'Description', 'Tags'],
                    rows=rows,
                    footers=["Footer 1", "Footer 2", "Footer 3"],
                    variant="striped",
                )
            )
        ),
        padding="5em"
    )


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

app.add_page(Data, route="/data")
