"""Welcome to Reflex! This file outlines the steps to create a basic app."""

from rxconfig import config

import reflex as rx


class State(rx.State):
    """The app state."""


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


def navbar():
    """The navbar for the top of the page."""
    return rx.chakra.box(
        rx.chakra.hstack(
            rx.chakra.hstack(
                rx.chakra.image(src="/favicon.ico", width="50px"),
                rx.heading("Osama Abd El Mohsen"),

            ),
            # rx.hstack(
            #     # rx.color_mode.icon(),
            #     # rx.color_mode.switch(),
            #     rx.chakra.menu(
            #         rx.chakra.menu_button(
            #             "Cont", bg="black", color="white", border_radius="md", px=4, py=2
            #         ),
            #         rx.chakra.menu_list(
            #             rx.chakra.link(
            #                 rx.chakra.menu_item(
            #                     rx.chakra.hstack(rx.chakra.text(
            #                         "Customers"), rx.chakra.icon(tag="hamburger"))
            #                 ),
            #                 href="/",
            #             ),
            #             rx.chakra.menu_divider(),
            #             rx.chakra.link(
            #                 rx.chakra.menu_item(
            #                     rx.chakra.hstack(rx.chakra.text(
            #                         "Onboarding"), rx.chakra.icon(tag="add"))
            #                 ),
            #                 href="/onboarding",
            #             ),
            #         ),
            #     ),
            #     align='center'
            # ),
            justify="space-between",
            padding_x="2em",
            padding_y="1em",
            box_shadow="lg",
        ),
        position="fixed",
        width="100%",
        top="0px",
        z_index="500",
    )


def skill(skillName: str, precentage: int):
    return rx.card(
        rx.inset(
            rx.image(
                src="/Netflix_Dashboard_tableau.png",
                width="1200px",
                height="auto",
            ),
            side="top",
            pb="current",
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
            value=precentage,
            max=100
        ),
        rx.divider(),
        spacing='10',
    )


def index() -> rx.Component:
    return rx.chakra.center(
        rx.chakra.vstack(
            navbar(),
            rx.image(
                src="https://readme-typing-svg.herokuapp.com/?lines=Mechatronics%20Engineer;Always%20learning%20new%20things&font=Fira%20Code&center=true&width=440&height=45&color=3DB54A&vCenter=true&size=22"
            ),
            rx.card(
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
                            rx.chakra.heading("P"),
                            rx.chakra.heading("Y"),
                            rx.chakra.heading("T"),
                            rx.chakra.heading("H"),
                            rx.chakra.heading("O"),
                            rx.chakra.heading("N"),
                            direction="column",
                            spacing="3",
                            width='80%',
                            size="3xl"
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
                                CardSwitcherState.cards[CardSwitcherState.current_card_index], 50),
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
                    footer=rx.chakra.heading("Footer", size="sm"),
                    font_size="2em",
                    font_family= "Vollkorn"
                ),
                variant='ghost',
                
            ),
        ),
        padding="5em"
    )


class CardSwitcherState(rx.State):
    current_card_index: int = 0
    cards = ["Python", "C", "HTML"]  # Example cards

    def next_card(self):
        if self.current_card_index < len(self.cards) - 1:
            self.current_card_index += 1

    def previous_card(self):
        if self.current_card_index > 0:
            self.current_card_index -= 1


app = rx.App(
    style=style,
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Vollkorn&display=swap",
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
# app.add_page(card_switcher, route="/c")
