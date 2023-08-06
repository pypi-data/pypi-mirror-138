#!/opt/homebrew/bin/python3

from email import header
from email.utils import parsedate
# from itertools import filterfalse
import typer
import pathlib2
import json
import sys
from datetime import datetime, timedelta
from datetime import date
from dateutil.rrule import rrule, MONTHLY
import cairo
import yaml



# GLOBAL CONSTANTS
__version__ = "1.2.1"
__date__ = "Feb-2022"

background = 0
middleground = 1
foreground = 2
colors = {"white": "#ffffff", "red": "#fbd8ea", "blue": "#c4e2fa", "yellow": "#fff4d6", "violet": "#dad0ef", "green": "#edf5dc", "aqua": "#d4f3f6"}


# FUNCTIONS

def parse_date(d: str):
    try:
        dt = datetime.strptime(d, "%d-%b-%Y")
        return(date(dt.year, dt.month, dt.day))
    except ValueError:
        pass
    try:
        dt = datetime.strptime(d, "%b-%Y")
        return(date(dt.year, dt.month, 15))
    except ValueError:
        raise ValueError('no valid date format found')


def get_timepoints(timepoints):
    out = []
    for i in timepoints:
        if "date" in i.keys():
            out.append(i)
        elif "timepoints" in i.keys():
            out += get_timepoints(i["timepoints"])
    return(out)


def get_dates(timepoints):
    return(i["date"] for i in get_timepoints(timepoints))


def all_dates(blocks):
    return([parse_date(i) for b in blocks for th in b["threads"] for i in get_dates(th["timepoints"])])


def max_date(blocks):
    return(max(all_dates(blocks)))


def min_date(blocks):
    return(min(all_dates(blocks)))


def quarter(ref):
    """return quarter of date. Date is provided as datetime object"""
    quarters = [("1-Jan", "31-Mar"),("1-Apr", "30-Jun"), ("1-Jul", "30-Sep"), ("1-Oct", "31-Dec")]
    borders = [(parse_date(start + "-" + str(ref.year)), parse_date(end + "-" + str(ref.year))) for (start, end) in quarters]
    for i, (s, e) in enumerate(borders, start=1):
        if ref >= s and ref <= e:
            return((i, ref.year))
    raise ValueError(f'date {ref} not in quarters')


# ELEMENTARY RENDERING FUNCTINOS

def svg_line(x1, y1, x2, y2, lwd=1, color="black", dashed=False):
	dash = f'stroke-dasharray: {lwd*3} {lwd*3}' if dashed else ""
	return(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" style="stroke:{color}; stroke-width:{lwd}; {dash}" />\n')


def svg_rect(x, y, w, h, lwd=1, fill_color="none", line_color="black", fill_opacity=0):
    return(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" style="stroke:{line_color};  stroke-width:{lwd}; fill:{fill_color}; fill-opacity:{1 - fill_opacity}" />\n')


def svg_circle(x, y, r, lwd=1.2, fill_color="none", line_color="black"):
	return(f'<circle cx="{x}" cy="{y}" r="{r}" style="stroke:{line_color};  stroke-width:{lwd}; fill:{fill_color};"/>\n')


def svg_text(x, y, text, css_class="", font_weight="normal"):
	if css_class:
		return(f'<text x="{x}" y="{y}" font-weight="{font_weight}" class="{css_class}">{text}</text>\n')
	else:
		return(f'<text x="{x}" y="{y}" font-weight="{font_weight}">{text}</text>\n')


def svg_path(x, y, points, lwd=1, size=1, fill=False, dashed=False, fill_color="none", title=""):
	title=""
	dash = "stroke-dasharray: 2.5 2.5" if dashed else ""
	(x1, y1) = points[-1]
	out = f'<path d="M{x1*size+x}, {y1*size+y} '
	for (x2, y2) in points:
		out += f'L{x2*size+x}, {y2*size+y} '
	out += f'Z" style="stroke: black; fill: {fill_color}; stroke-width:{lwd}; {dash}"'
	if title != "":
		out += f'><title>{title}</title></path>'
	else:
		out += ' />'
	return(out)


def svg_symbol(x, y, width, symbol, size=1, fill=False, fill_color="none", **kwargs):
    if symbol == "diamond":
        return svg_path(x, y, [(0,-0.5), (0.25, 0), (0, 0.5), (-0.25, 0)], size=size*1.4, fill=fill, fill_color=fill_color, **kwargs)
    elif symbol == "block":
        w = width/size/1.5*.7
        return svg_path(x, y, [(w/-2, -.25), (w/2, -.25), (w/2, .25), (-w/2, .25)], size=size*1.5, fill=fill, fill_color=fill_color, **kwargs)
    elif symbol == "arrow":
        return svg_path(x, y, [(-0.03, -0.5), (0.03, -0.5), (0.03, 0), (0.1875, 0), (0.0, 0.5), (-0.1875, 0), (-0.03, 0)], size=size*1.2, fill=True, fill_color="black", **kwargs)
    elif symbol == "circle":
        return svg_circle(x, y, width/2*size, fill_color=fill_color, **kwargs)
    return ""


def svg_large_arrow(x1, x2, y, height, metrics, style, **kwargs):
    (textwidth_function, textheight_function, date_position_function, month_width, text_height, lineheight, min_scale_date, max_scale_date) = metrics
    (lwd, xpadding, ypadding, threadoffset, linescaling) = style
    
    points = [(x1, y-height/2), (x2-height, y-height/2), (x2-height, y-height), (x2, y), (x2-height, y+height), (x2-height, y+height/2), (x1, y+height/2)]
    return(svg_path(0, 0, points, **kwargs))


def svg_fine_arrow(x1, x2, y, height, **kwargs):
    head_length = 9
    head_width = 2.7
    points = [(x1, y+height/2), (x2-height*head_length, y+height/2), (x2-height*head_length, y+height*head_width), (x2, y), (x2-height*head_length, y-height*head_width), (x2-height*head_length, y-height/2), (x1, y-height/2)]
    return(svg_path(0, 0, points, **kwargs))


def month_between(start, end):
    """return the date difference between start and end in months"""
    start.replace(day=1)
    end.replace(day=1)
    return([dt.date() for dt in rrule(MONTHLY, dtstart=start, until=end)])


def month_difference(start, end):
    """return the date difference between start and end in months"""
    return(len(month_between(start, end))-1)


# RENDERING FUNCTIONS

def render_header(tl, metrics, style, xoffset, yoffset=0):
    """render the header including the year labels and month scale"""
    (textwidth_function, textheight_function, date_position_function, month_width, text_height, lineheight, min_scale_date, max_scale_date) = metrics
    (lwd, xpadding, ypadding, threadoffset, linescaling) = style

    month_grid = month_width > textwidth_function("XX") 
    month_names = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]

    month_list = month_between(min_scale_date, max_scale_date)
    year_list = list(dict.fromkeys([i.year for i in month_between(min_scale_date, max_scale_date)]))
    svg_back = ""
    y = yoffset

    # render year labels
    for yr in year_list:
        dec_date = date(yr, 12, 1)
        if dec_date > min(month_list) and dec_date < max(month_list):
            dec = date_position_function(dec_date)
            svg_back += svg_line(dec + month_width, y, dec+month_width, y+lineheight, lwd=lwd)

        start = len(month_list)
        end = 0
        for i, v in enumerate([i.year == yr for i in month_list], start=0):
            if v and i < start:
                start = i
            if v and i > end:
                end = i
        year_start = date_position_function(month_list[start])
        year_end = date_position_function(month_list[end])
        if year_end - year_start > textwidth_function(str(yr)):
            svg_back += svg_text(year_start+(year_end-year_start+month_width-textwidth_function(str(yr)))/2, y+lineheight-(lineheight-text_height)/2, str(yr), font_weight="normal")             
    y += lineheight + ypadding

    month_height = lineheight * 1.2

    if month_grid:
    # render month grid
        for i, x in enumerate(month_between(min_scale_date, max_scale_date)[:-1], start=0):
            fill = "none" if (quarter(date(x.year, x.month, x.day))[0] % 2) else colors["violet"]
            svg_back += svg_rect(xoffset + i * month_width, y, month_width, month_height, fill_color=fill, lwd=style[0])
            svg_back += svg_text(xoffset + i * month_width + (month_width - textwidth_function(month_names[x.month-1]))/2, y + month_height - (month_height-text_height)/2, month_names[x.month-1])
    else:
        # render quarter grid
        m = month_list[0]
        last_quarter = quarter(date(m.year, m.month, m.day))
        last_x = date_position_function(month_list[0])
        for m in [i for i in month_list]:
            q = quarter(date(m.year, m.month, m.day))
            if q != last_quarter:
                current_x = date_position_function(m)
                fill = colors["violet"]if q[0] % 2 else "none"
                svg_back += svg_rect(last_x, y, current_x - last_x, month_height, lwd=lwd, fill_color=fill)
                label = f'Q{last_quarter[0]}'
                if textwidth_function(label) + textwidth_function("X") < current_x - last_x:
                    svg_back += svg_text(last_x + (current_x-last_x-textwidth_function(label))/2, y + month_height - (month_height-text_height)/2, label)
                last_quarter = q
                last_x = current_x

    y += month_height + ypadding * 2
    return([svg_back, "", "", y, xoffset + (len(month_list)-1) * month_width])
    

def render_month_grid(tl, metrics, style, xoffset, starty, endy):
    (textwidth_function, textheight_function, date_position_function, month_width, text_height, lineheight, min_scale_date, max_scale_date) = metrics
    (lwd, xpadding, ypadding, threadoffset, linescaling) = style

    svg_out = ""
    month_list = [date_position_function(i) for i in month_between(min_scale_date, max_scale_date)]

    for i in range(0, len(month_list)):
        if not i % 2:
            svg_out += svg_rect(month_list[i], starty, month_width, endy-starty, fill_color="white", fill_opacity=0.6, line_color="none")
    return(svg_out)


def short_date_string(d: date):
    temp = parse_date(d)
    return(temp.strftime("%d-%b"))


def render_twolines(date_string, y, text1, text2, metrics, xnudge=0, align="center"):
    """render date and caption in two lines

    :param date_string: date for x positioning in string format
    :param y:       y position for first line
    :param text1:   upper line, i.e., date string
    :param text2:   lower line, i.e., caption
    :param xnudge:  offset value for right or left align
    :return:        tuple: (svg output, maximal x)    
    """
    (textwidth_function, textheight_function, date_position_function, month_width, text_height, lineheight, min_scale_date, max_scale_date) = metrics

    x = date_position_function(parse_date(date_string))
    y = y + textheight_function("X") + textheight_function("X")/2

    if align == "center":
        return((svg_text(x - textwidth_function(text1)/2, y, text1)
            + svg_text(x - textwidth_function(text2)/2, y + textheight_function("X") * 1.7, text2)),
            max(x + textwidth_function(text1)/2, x + textwidth_function(text2)/2))
    if align == "right":
        return((svg_text(x - textwidth_function(text1) + xnudge, y, text1)
            + svg_text(x - textwidth_function(text2) + xnudge, y + textheight_function("X") * 1.7, text2)),
            x + xnudge)
    if align == "left":
        return((svg_text(x - xnudge, y, text1)
            + svg_text(x - xnudge, y + textheight_function("X") * 1.7, text2)),
            max(x + textwidth_function(text1), x + textwidth_function(text2)))
    return(("", x))


def alignment_solution(time_points, reference, metrics, xpadding=0, xnudge=0, short_date=False):
    (textwidth_function, textheight_function, date_position_function, month_width, text_height, lineheight, min_scale_date, max_scale_date) = metrics
    """calculates the best alignment solution for time points
    
    :param time_points: list of time points to be aligned
    :param reference:   list of target alignments of the same length as the time_points
    :param metrics:     the metrics
    :param xpadding:    the minimum padding between labels
    :param xnudge:      the width that a right-align is shifted to the right and a left-align to the left, relative to the target coordinate
    
    All possible arrangement of the date labels being aligned eigher left, right or center relative to the x-coordinate of the respective date are created. When the respective individual label alignment collides on the right or left side with the previous date or on the left with the previous label text, no alignment is assigned. In a second step, all sequences are compared with a reference alignment and ordered by the lowest deviations from it, the lowest number of non-alignments, the highest number of center alignments, the highest number of left alignments, and the highest number of right alignments, in this order.
    The best sequence is returned as the alignment solution.
    """
    def _alg_solution(x: list, w: list, sequences: list):
        """x is the list of timepoint positions, w is the list of label widths"""
        if len(x) == 0:
            return(sequences)
        else:
            xx = x.pop(0)
            ww = w.pop(0)
            out = []
            for s in sequences:
                options = []
                last_x = s[0]
                next_x = x[0] if len(x) > 0 else 1000000
                if xx - ww/2 >= last_x and xx + ww/2 + xpadding < next_x:
                    options.append((xx + ww/2 + xpadding, "center"))
                if xx - ww >= last_x:
                    options.append((xx + xnudge + xpadding, "right"))
                if xx - xnudge > last_x and xx - xnudge + ww + xpadding < next_x:
                    options.append((xx - xnudge + ww + xpadding, "left"))
                if len(options) == 0:
                    options.append((xx, ""))
                for o in options:
                    out.append((o[0], s[1] + [o[1]]))
            return(_alg_solution(x, w, out))

    x = [date_position_function(parse_date(i["date"])) for i in time_points]
    if short_date:
        w = [max(textwidth_function(short_date_string(i["date"])), textwidth_function(i["caption"])) for i in time_points]
    else:
        w = [max(textwidth_function(i["date"]), textwidth_function(i["caption"])) for i in time_points]
    # w = [max(textwidth_function(i["date"]), textwidth_function(i["caption"])) for i in time_points]
    temp = _alg_solution(x, w, [(0,[])])
    sequences = []
    for s in [i[1] for i in temp]:
        matches = [ss == rr for ss, rr in zip(s, reference) if rr != ""]
        n_match = sum(matches)
        n_nonvoid = sum([i != "" for i in s])
        n_center = sum([i == "center" for i in s])
        n_left = sum([i == "left" for i in s])
        n_right = sum([i == "right" for i in s])
        sequences.append((n_match, n_nonvoid, n_center, n_left, n_right, s))
    sorted_sequences = sorted(sequences, key=lambda x: (x[0], x[1], x[2], x[3], x[4]), reverse=True)
    return([(d, a) for d, a in zip(time_points, sorted_sequences[0][5])])


def bottom_alignment_solution(top_solution, metrics, xpadding=0, xnudge=0, short_date=False):
    (textwidth_function, textheight_function, date_position_function, month_width, text_height, lineheight, min_scale_date, max_scale_date) = metrics
    
    timepoints = []
    reference = []
    for i in range(0, len(top_solution)):
        (tp, align) = top_solution[i]
        next_align = top_solution[i+1][1] if i < len(top_solution)-1 else "center"
        prev_align = top_solution[i-1][1] if i > 0 else "center"
        next_x = top_solution[i+1][0]["date"] if i < len(top_solution)-1 else top_solution[-1][0]["date"]
        prev_x = top_solution[i-1][0]["date"] if i > 0 else top_solution[0][0]["date"]
        if align == "":
            timepoints.append(tp)
            r = "center"
            if next_align == "left":
                if prev_align == "right":
                    x1 = date_position_function(parse_date(prev_x))
                    x2 = date_position_function(parse_date(next_x))
                    x = date_position_function(parse_date(tp["date"]))
                    if x - x1 > x2 - x:
                        r = "right"
                    else:
                        r = "left"
                else:
                    r = "right"
            if prev_align == "right" and next_align != "left":
                r = "left"
            reference.append(r)  
    return(alignment_solution(timepoints, reference, metrics, xpadding=xpadding, xnudge=xnudge))


def render_segment(thread, y, metrics, style):
    (textwidth_function, textheight_function, date_position_function, month_width, text_height, lineheight, min_scale_date, max_scale_date) = metrics
    (lwd, xpadding, ypadding, threadoffset, linescaling) = style

    def make_segment(out, lastx, tps, seg_style=""):
        for tp in tps:
            if "date" in tp:
                currentx = date_position_function(parse_date(tp["date"]))
                if lastx != 0:
                    if seg_style == "smallarrow":
                        if currentx - lastx - 2 * xpadding > 9:
                            out += svg_fine_arrow(lastx+xpadding, currentx-xpadding, y+lineheight/2, linescaling * 0.9, lwd=lwd, fill_color="black")
                    elif seg_style == "largearrow":
                        arrowheight = lineheight * 0.6
                        if currentx - lastx - 2 * xpadding > arrowheight:
                            out += svg_large_arrow(lastx+xpadding, currentx-xpadding, y+lineheight/2, arrowheight, metrics, style, lwd=lwd, fill_color="white")
                lastx = currentx
            elif "timepoints" in tp and len(tp["timepoints"]):
                currentx = date_position_function(parse_date(tp["timepoints"][0]["date"]))
                if seg_style == "smallarrow":
                    if currentx - lastx - 2 * xpadding > 9:
                        out += svg_fine_arrow(lastx+xpadding, currentx-xpadding, y+lineheight/2, 0.9 * linescaling, lwd=lwd, fill_color="black")
                if seg_style == "largearrow":
                    arrowheight = lineheight * 0.6
                    if currentx - lastx - 2 * xpadding > arrowheight:
                        out += svg_large_arrow(lastx+xpadding, currentx-xpadding, y+lineheight/2, arrowheight, metrics, style, lwd=lwd, fill_color="white")
                (o, l) = make_segment(out, 0, tp["timepoints"], tp["style"])
                out += o
                lastx = l
        return((out, lastx))
    
    (out, _last) = make_segment("", 0, thread["timepoints"], "")
    return(out)


def render_thread(thread, metrics, style, xoffset, yoffset=0, short_date=True):
    (textwidth_function, textheight_function, date_position_function, month_width, text_height, lineheight, min_scale_date, max_scale_date) = metrics
    (lwd, xpadding, ypadding, threadoffset, linescaling) = style

    xnudge = textwidth_function("n")
    datepadding = textwidth_function("m")
    svg_out = ""
    
    y = yoffset

    if "timepoints" in thread.keys():
        thread_tps = get_timepoints(thread["timepoints"])
        reference = ["center"] * len(thread_tps)

        top_alignments = alignment_solution(thread_tps, reference, metrics, xpadding=datepadding, xnudge=xnudge, short_date=short_date)
        bottom_alignments = bottom_alignment_solution(top_alignments, metrics, short_date=short_date)  
 
        # render top labels
        max_x = 0
        for (tp, a) in top_alignments:
            d = short_date_string(tp["date"]) if short_date else tp["date"]
            # (svg, x) = render_twolines(tp["date"], y, tp["date"], tp["caption"], metrics, xnudge=xnudge, align=a)
            (svg, x) = render_twolines(tp["date"], y, d, tp["caption"], metrics, xnudge=xnudge, align=a)
            svg_out += svg
            max_x = max(max_x, x)
        y += textheight_function("X") * 1.7 + lineheight + ypadding * 1.5

        # render thread caption
        svg_out += svg_text(threadoffset + xpadding * 2, y + (lineheight+textheight_function("X"))/2, thread["caption"], font_weight="normal")

        # render symbols
        for tp in thread_tps:
            if "date" in tp.keys():
                svg_out += svg_symbol(date_position_function(parse_date(tp["date"])), y + lineheight/2, 10, "diamond", text_height*1.3, lwd=lwd, fill_color="white")

        # render segments
        svg_out += render_segment(thread, y, metrics, style)

        y += lineheight + ypadding * 0.5

        # render bottom labels, if applicable
        if bottom_alignments:
            for tp, a in bottom_alignments:
                d = short_date_string(tp["date"]) if short_date else tp["date"]
                # (svg, x) = render_twolines(tp["date"], y, tp["date"], tp["caption"], metrics, xnudge=xnudge, align=a) 
                (svg, x) = render_twolines(tp["date"], y, d, tp["caption"], metrics, xnudge=xnudge, align=a) 
                svg_out += svg
                max_x = max(max_x, x)
            y  += lineheight * 2
    return(["", "", svg_out, y + ypadding, max_x])


def render_block(block, header_width, metrics, style, xoffset, yoffset=0, short_date=False):
    """render block structure and threads included"""
    (textwidth_function, textheight_function, date_position_function, month_width, text_height, lineheight, min_scale_date, max_scale_date) = metrics
    (lwd, xpadding, ypadding, threadoffset, linescaling) = style

    y_top = yoffset
    # out = ["", "", svg_text(5 + xpadding, y_top + lineheight, block["caption"], font_weight="bold"), yoffset + ypadding, 0]
    out = ["", "", svg_text(xpadding, y_top + lineheight, block["caption"], font_weight="bold"), yoffset + ypadding, 0]

    for thd in block["threads"]:
        out = add_rendering(out, render_thread, thd, metrics, style, xoffset, short_date=short_date)
    out[-2] += ypadding
    y_bottom = out[-2]
    # out[background] = svg_rect(5, y_top, header_width-5, y_bottom-y_top, lwd=0, fill_color=colors[block["color"]], fill_opacity=0.4)
    out[background] = svg_rect(0, y_top, header_width, y_bottom-y_top, lwd=0, fill_color=colors[block["color"]], fill_opacity=0.4)
    out[-2] += ypadding
    return(out)


def add_rendering(old, rendering_function, *args, **kwargs):
    new = rendering_function(*args, yoffset=old[-2], **kwargs)
    return([o + n for o, n in zip(old[:-2], new[:-2])] + [new[-2], max(old[-1], new[-1])])


def month_start(date):
    return(date.replace(day=1))


def next_month_start(date):
    return(date.replace(month=date.month + 1, day=1))


def render_tl(tl, fontsize=14, font="Arial", monthwidth=1, today=False, autowidth=False, datelines=False, grid="", linescaling=1, mindate=0, maxdate=0, short_date=False):
    # init canvas for text metrics, make metrics
    canvas = cairo.Context(cairo.SVGSurface("temp.svg", 10, 10))
    canvas.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    canvas.set_font_size(fontsize)

    def make_textwidth(canvas):
        def textwidth_function(text):
            return(canvas.text_extents(str(text))[2])
        return(textwidth_function)

    def make_textheight(canvas):
        def textheight_function(text):
            return(canvas.text_extents(text)[3])
        return textheight_function

    textheight_function = make_textheight(canvas)
    textwidth_function = make_textwidth(canvas)

    lineheight = textheight_function("X") * 1.7

    ypadding = lineheight/3
    xpadding = textwidth_function("X")

    max_block_caption_width = max([textwidth_function(b["caption"]) for b in tl["blocks"]])
    max_thread_caption_width = max([textwidth_function(t["caption"]) for b in tl["blocks"] for t in b["threads"]])
    threadoffset = max_block_caption_width/3 + 2 * xpadding

    # xoffset = 5 + max_block_caption_width/3 + max_thread_caption_width + xpadding * 4
    xoffset = max_block_caption_width/3 + max_thread_caption_width + xpadding * 4
    # yoffset = 5
    yoffset = 0
    lwd = 1.5 * linescaling

    # Date limits
    if mindate:
        min_scale_date = month_start(mindate)
    else:
        min_scale_date = (min_date(tl["blocks"]).replace(day=1) - timedelta(1)).replace(day=1)
    if maxdate:
        max_scale_date = next_month_start(maxdate)
    else:
        max_scale_date = (max_date(tl["blocks"]).replace(day=1) + timedelta(32)).replace(day=1)

    if min_scale_date >= max_scale_date:
        raise ValueError("Mindate must be before maxdate!")

    month_width = 30 * monthwidth
    if autowidth:
        month_width = (1200 -xoffset) / len(month_between(min_scale_date, max_scale_date))

    def date_position_function(d):
        month_x = month_difference(min_scale_date, d) * month_width
        day_x = (d.day-1)/30 * month_width  # 30 is simplified but good enough...
        return(xoffset + month_x + day_x)

    metrics = (textwidth_function, textheight_function, date_position_function, month_width, textheight_function("X"), lineheight, min_scale_date, max_scale_date)
    style = (lwd, xpadding, ypadding, threadoffset, linescaling)

    # Rendering
    render_out = ["", "", "", yoffset, 0]  # render_out is: [background, middleground, foreground, y, max_x]

    # render header
    render_out = add_rendering(render_out, render_header, tl, metrics, style, xoffset)

    header_width = render_out[-1]
    header_bottom = render_out[-2]

    # render blocks
    for b in tl["blocks"]:
        render_out = add_rendering(render_out, render_block, b, header_width, metrics, style, xoffset, short_date=short_date)

    # render month grid
    if grid:
        render_out[1] += render_month_grid(tl, metrics, style, xoffset, header_bottom, render_out[-2])
    
    # render datelines
    dls = ""
    if datelines:
        ds = [date_position_function(i) for i in all_dates(tl["blocks"])]
        for d in ds:
            dls += svg_line(d, header_bottom-ypadding, d, render_out[-2], lwd=lwd, color="#ccc")
    if today:
        today = date_position_function(date.today())
        dls += svg_line(today, header_bottom-ypadding, today, render_out[-2], lwd=lwd, color="red")
    render_out[middleground] = dls + render_out[middleground]
    render_out[-1] += textwidth_function("X")

    return([render_out[0] + render_out[1] + render_out[2], render_out[-2], render_out[-1]])


def datefilter(blocks, filter_function):
    out = blocks

    def _filter_tps(tps):
        out = []
        for tp in tps:
            if "date" in tp.keys():
                if filter_function(parse_date(tp["date"])):
                    out.append(tp)
            if "timepoints" in tp.keys():
                tp["timepoints"] = _filter_tps(tp["timepoints"])
                out.append(tp)
        return(out)

    for b in out:
        for t in b["threads"]:
            t["timepoints"] = _filter_tps(t["timepoints"])
    return(out)



# MAIN

app = typer.Typer(add_completion=False)


def version_callback(value: bool):
    if value:
        typer.echo(f'version {__version__} ({__date__})')
        raise typer.Exit()


@app.command()
def main(
    file: str = typer.Argument(...),
    fontsize: float = typer.Option(18, "--fontsize", "-s", help="Font size"),
    font: str = typer.Option("Arial", "--font", "-f", help="Font type"),
    monthwidth: float = typer.Option(1, "--monthwidth", "-m", help="Month width scaler"),
    mindate: str = typer.Option("", "--min-date", "-i", help="Minimum cutoff date"),
    maxdate: str = typer.Option("", "--max-date", "-x", help="Maximum cutoff date"),
    today: bool = typer.Option(False, "--show-today", "-t", help="Mark today"),
    grid:  bool = typer.Option(False, "--show-grid", "-g", help="Show month grid"),
    datelines: bool = typer.Option(False, "--show-datelines", "-d", help="Show datelines"),
    autowidth: bool = typer.Option(False, "--autowidth", "-a", help="Render width automatically"),
    linescaling: float = typer.Option(1, "--line-scaling", "-l", help="Line width scaling factor"),
    all: bool = typer.Option(False, "--all", "-A", help="All options, equivalent to -atg"),
    shortdate: bool = typer.Option(False, "--short-date", "-r", help="Show only month and year in date lables"),
    output: str = typer.Option("", "--output", "-o", help="Output file name"),
    debug: bool = typer.Option(False, "--debug", "-D", help="Show debug output"),
    version: bool = typer.Option(False, "--version", help="Show version and exit", callback=version_callback)):
    """TL: Timeline figures


    Generates a timeline view, e.g., for clinical trials, based on a json- or yaml-formatted input FILE. Graphical output is provided in svg vector format that can be rendered by any webbrowser or directly imported into Office applications. Use below OPTIONS to manage the output style.

    This program comes with ABSOLUTELY NO WARRANTY.	This is free software, and you are welcome to redistribute it under certain conditions.

    TL is proudly written in functional Python. Copyright (C) Rainer Strotmann 2022. Version information under 'tl --version'
    """

    if all:
        autowidth = True
        today = True
        grid = True

    # make output file
    infile = pathlib2.Path(file)
    inpath = pathlib2.Path(file).resolve().parent
    # outfile = inpath.joinpath(infile.stem + ".svg")

    if output:
        outpath = pathlib2.Path.cwd().joinpath(output)
        if outpath.is_dir():
            outfile = outpath.joinpath(infile.stem + ".svg")
        else:
            outfile = outpath
    else:
        outfile = inpath.joinpath(infile.stem + ".svg")

    # read input file
    try:
        with open(infile) as f:
            tl = json.load(f)
    except json.decoder.JSONDecodeError as err:
        try:
            with open(infile) as f:
                tl = yaml.safe_load(f)
        except:
            sys.exit(f'Syntax error in input file {infile}:\n{err}')
    except FileExistsError  :
        sys.exit("Error loading input file")
    if "blocks" not in tl:
        sys.exit("no blocks in input file")
    else:
        blocks = tl["blocks"]
    
    # debug
    if debug:
        print(json.dumps(tl, indent=2))
        print("---")
        print(yaml.dump(tl))

    # date filtering
    if (mindate and maxdate) and parse_date(maxdate) <= parse_date(mindate):
        sys.exit("Date error: Maxdate must be after mindate")

    if maxdate:
        blocks = datefilter(blocks, lambda x: x <= parse_date(maxdate))
        max_scale_date = parse_date(maxdate)
    elif "max-date" in tl.keys():
        blocks = datefilter(blocks, lambda x: x <= parse_date(tl["max-date"]))
        max_scale_date = parse_date(tl["max-date"])
    else:
        max_scale_date = 0

    if mindate:
        blocks = datefilter(blocks, lambda x: x >= parse_date(mindate))
        min_scale_date = parse_date(mindate)
    elif "min-date" in tl.keys():
        blocks = datefilter(blocks, lambda x: x >= parse_date(tl["min-date"]))
        min_scale_date = parse_date(tl["min-date"])
    else:
        min_scale_date = 0

    # rendering
    try:
        ([svg_out, y, max_x]) = render_tl(tl, fontsize=fontsize, monthwidth=monthwidth, today=today, autowidth=autowidth, datelines=datelines, grid=grid, linescaling=linescaling*1.2, mindate=min_scale_date, maxdate=max_scale_date, short_date=shortdate)

        # adding svg boilerplate
        title = infile.stem
        viewport_width = max_x
        viewport_height = y

        svg_out = f'<svg width="{viewport_width}" height="{viewport_height}" viewbox="0 0 1600 {viewport_height/viewport_width}" xmlns="http://www.w3.org/2000/svg">\n<style>text {{font-family: {font}; font-size: {fontsize}px ;}}</style>\n<desc>Timeline graph autogenerated by tl version {__version__} ({__date__}), author: Rainer Strotmann</desc><title>{title}</title>' + svg_out + '\n</svg>'

        # save to file
        with open(outfile, "w") as f:
            f.write(svg_out)

    except ValueError as err:
        sys.exit(f'Error: {err}')

if __name__ == "__main__":
	app()
    