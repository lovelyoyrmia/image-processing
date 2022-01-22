from modules.sendEmail import SendEmail


class Navigation:
    def __init__(self, st):
        self.st = st

    def welcome(self):
        self.st.image("assets/logo.png", width=200)
        self.st.markdown(
            """
        ### Web Application that shows different image processing algorithms such as
        - Gray Scale
        - Contrast
        - Blurring
        - Brightness
        - Thresholding
        - Hue and Saturation
        - Cartoonize Image
        - Remove Background

        ### Also this website has Computer Vision Features such as
        - Face Detection
        - Smile Detection
        - Body and Object Detection
        - Mask R-CNN Image
        """
        )

    def aboutPage(self):
        self.st.markdown(
            """
            ### Follow me on

            <link
                rel="stylesheet"
                href="https://use.fontawesome.com/releases/v5.15.4/css/all.css"
                integrity="sha384-DyZ88mC6Up2uqS4h/KRgHuoeGwBcD4Ng9SiP4dIRy0EXTlnuz47vAwmeGwVChigm"
                crossorigin="anonymous"
            />
            
            <div class='icon-container'>
                <a href='https://github.com/lovelyoyrmia' target='_blank' rel='noopener noreferrer'><i class='fab fa-github'></i></a>
                <a href='https://www.instagram.com/lovelyoyrmia/' target='_blank' rel='noopener noreferrer'><i class='fab fa-instagram'></i></a>
                <a href='https://www.linkedin.com/in/lovelyoyrmia' target='_blank' rel='noopener noreferrer'><i class='fab fa-linkedin'></i></a>
            </div>
            <h5>Created with ❤ by Lovelyo Yeremia</h5>
            <a href='https://lovelyoyrmia.github.io' class='link-web' target='_blank' rel='noopener noreferrer'>Portfolio Website</a>

            <style>
            .icon-container a {
                text-decoration: none;
                color: #2235d2;
                font-size: 2rem;
            }
            .icon-container {
                display: flex;
                width: 30%;
                justify-content: space-between;
            }
            .icon-container a:hover {
                color: rgba(0, 0, 255, 0.7);
            }
            h5 {
                margin-top: 2rem;
            }
            .link-web {
                font-size: 25px;
                font-weight: 600;
                text-decoration: none;
            }
            </style>
        """,
            unsafe_allow_html=True,
        )

    def contact(self):
        self.st.subheader("Let's get in touch")
        self.st.image("assets/images.jpg", width=400)
        email = self.st.text_input("Enter your email")
        if self.st.button("Subscribe"):
            send = SendEmail(self.st)
            with self.st.spinner("Sending email..."):
                send.sendEmail(email)
