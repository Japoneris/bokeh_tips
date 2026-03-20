from bokeh.plotting  import ColumnDataSource, figure, output_file, show
from bokeh.models    import HoverTool, CustomJS
from bokeh.layouts   import column, row

from bokeh.models import Spinner

import numpy as np

if __name__ == "__main__":
    

    year_max = 20
    r_fee = 0.03
    r_div = 0.05
    C_invest0 = 100
    C_house = 200
    S_earn = 10
    S_save = 10
    
    def savings(alpha=0.1):

        C_invest = C_invest0
        C_used = C_invest*alpha

        C_loan  = C_house - C_used
        C_invest = C_invest - C_used

        years = C_loan / S_earn
        fees = (C_loan) * r_fee * (years+1) / 2


        S_save_0 = S_save - fees/years # How much you can save during the first period
        S_save_1 = S_save + S_earn # How much you can save during the second period with no fees


        C1 = C_invest + S_save_0 * years
        C2 = C1 + (year_max - years) * S_save_1

        D0 = (C_invest + C1) * years * r_div / 2
        D1 = (C1 + C2) * (year_max - years) * r_div / 2

        return C2, D0 + D1

    
    #TODO
    x_range = np.linspace(0, 1, 101)
    y_tot = []
    y_div = []
    y_cap = []
    for x in x_range:
        c, d = savings(x)
        y_div.append(d)
        y_cap.append(c)
        y_tot.append(d+c)
    
    source   = ColumnDataSource(data=dict(x=x_range, y=y_tot, y_div=y_div, y_cap=y_cap))
    
    
    W = 120
    
    spinner_year    = Spinner(title="Year max", low=1, high=30, step=1, value=year_max, width=W)
    spinner_saving  = Spinner(title="Saving per year", low=0,  high=50, step=0.1, value=S_save, width=W)
    spinner_salary  = Spinner(title="Salary per year", low=0,  high=50, step=0.1, value=S_earn, width=W)
    spinner_Fees    = Spinner(title="Loan fee (%)", low=0,  high=100, step=0.1,   value=r_fee*100, width=W)
    spinner_Div     = Spinner(title="Dividend rate (%)", low=0,  high=100, step=0.1, value=r_div*100, width=W)
    spinner_Capital = Spinner(title="Capital at t=0", low=0,  high=1000, step=1, value=C_invest0, width=W)
    spinner_Price   = Spinner(title="House price", low=0,  high=2000, step=1, value=C_house, width=W)
    
    
    #spinner.js_link('value', points.glyph, 'size')


    callback = CustomJS(args=dict(source=source,
        sp_year=spinner_year,
        sp_salary=spinner_salary,
        sp_saving=spinner_saving,
        sp_fees=spinner_Fees,
        sp_divs=spinner_Div,
        sp_capital=spinner_Capital,
        sp_price=spinner_Price,
        ),
                        code="""
        
        const data = source.data;
        
        
        const t2 = sp_year.value; // Considered timeline
        
        const capital = sp_capital.value; // initial capital
        const price = sp_price.value; // cost of the house
        
        const salary = sp_salary.value;
        const saving = sp_saving.value;
        
        const fees = sp_fees.value / 100;
        const divs = sp_divs.value / 100;
        
        for (var i=0; i < data.x.length; i++) {
            var alpha = data.x[i]; // rate in [0, 1]
            
            // How long does it take to reimburse ?
            var left_to_pay = Math.max(0, price - capital * alpha);
            var invested0   = capital - (price - left_to_pay); 
            var t1 = Math.min(t2, left_to_pay / salary);
            
            // How much left to invest ?
            var fees_tot = left_to_pay / 2 * (t1+1) * fees;
            var fees_per_year = fees_tot / t1;
            var invested1 = invested0 + (saving - fees_per_year) * t1
            
            // Dividends 
            var d1 = (invested0 + invested1) / 2 * t1 * divs;
            
            // T2
            var invested2 = invested1 + (saving + salary) * (t2 - t1)
            var d2 = (invested1 + invested2) / 2 * (t2 - t1) * divs;
            
            
            data.y[i] = d1 + d2 + invested2 
            data.y_div[i] = d1 + d2
            data.y_cap[i] = invested2
        }

        source.change.emit();
        """)
    
    spinner_year.js_on_change('value', callback)
    spinner_saving.js_on_change('value', callback)
    spinner_salary.js_on_change('value', callback)
    spinner_Fees.js_on_change('value', callback)
    spinner_Div.js_on_change('value', callback)
    spinner_Capital.js_on_change('value', callback)
    spinner_Price.js_on_change('value', callback)
    
    
    p = figure(plot_width=1000, plot_height=500,
            x_range=[-0.05, 1.05],
            #y_range=[0, 105],
            tools="pan,wheel_zoom,reset,save",
           title="Capital after investment.")

    # Plot circles. Define name for the item
    p.line('x', 'y', name="lines", source=source, line_width=3, line_alpha=0.7)#, legend_label="Total")
    #p.line('x', 'y_cap', source=source, line_width=2, line_alpha=0.7, color="red", legend_label="Capital invested")
    #p.line('x', 'y_div', source=source, line_width=2, line_alpha=0.7, color="green", legend_label="Dividends")

    hover = HoverTool(tooltips=[("Used to pay", '@x'), 
                                ("Amount obtained", "@y"),
                                ("- Dividend", "@y_div"),
                                ("- Capital", "@y_cap"),
                               ])
    p.add_tools(hover)

    #p.legend.location = "top_left"
    #p.legend.title = "Legend"

    p.xaxis.axis_label = 'Investment rate'
    p.yaxis.axis_label = 'k€'
    
    #p.xgrid.minor_grid_line_alpha = 0.4
    #p.xgrid.grid_line_alpha = 0.7
    #p.xgrid.ticker = [i*5 for i in range(19)]
    #p.xaxis.ticker = [i*5 for i in range(19)]

    output_file("output/investment_tradeoff.html", title="Money invested.")
    show(column(p, spinner_year, row(spinner_saving, spinner_salary), 
                row(spinner_Fees, spinner_Div),
                row(spinner_Price, spinner_Capital)))



    
    
    