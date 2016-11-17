

def add_colors_to_db(colors):
        """ Takes a list of comma-separated hex values, and makes a record in 
            Color if none existed previously """

        for color in colors:
            color_in_db = Color.query.filter(Color.color==color).first()
                # Color already in the table
                if color_in_db:
                # Color not in colors table
                else:
                    new_color = Color(color=color)
                    db.session.add(new_color)
                    db.session.commit()