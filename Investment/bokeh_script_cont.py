"""
Continuous investment
"""

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

        k_smooth = 50
        r1 = np.exp(np.log(1+r_div)/k_smooth)
        
        C1 = C_invest 
        
        for i in range(int(k_smooth*years)):
            C1 = C1 * r1 + S_save_0/k_smooth
        
        for i in range(int(k_smooth*years), k_smooth*year_max):
            C1 = C1 * r1 + S_save_1/k_smooth
        
        return C1

    
    #TODO
    x_range = np.linspace(0, 1, 101)
    y_tot = []
    for x in x_range:
        y_tot.append(savings(x))
    
    source   = ColumnDataSource(data=dict(x=x_range, y=y_tot))
    
    
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
        
        const k_split = 100;
        var r_divs = Math.exp(Math.log(1+divs)/k_split);
        
        for (var i=0; i < data.x.length; i++) {
            var alpha = data.x[i]; // rate in [0, 1]
            
            // How long does it take to reimburse ?
            var left_to_pay = Math.max(0, price - capital * alpha);
            var invested0   = capital - (price - left_to_pay); 
            var t1 = Math.min(t2, left_to_pay / salary);
            
            // How much left to invest ?
            var fees_tot = left_to_pay / 2 * (t1+1) * fees;
            var fees_per_year = fees_tot / t1;
            
            
            var invested1 = invested0;
            for (var j=0; j < t1*k_split; j++) {
                invested1 = invested1 * r_divs + (saving - fees_per_year)/k_split; 
            }
            
            for (var j=0; j < (t2-t1)*k_split; j++) {
                invested1 = invested1 * r_divs + (saving + salary)/k_split; 
            }
            
            data.y[i] = invested1;
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
            tools="pan,wheel_zoom,reset,save",
           title="Capital after investment.")

    # Plot circles. Define name for the item
    p.line('x', 'y', name="lines", source=source, line_width=3, line_alpha=0.7)#, legend_label="Total")

    hover = HoverTool(tooltips=[("Used to pay", '@x'), 
                                ("Amount obtained", "@y"),
                               ])
    p.add_tools(hover)


    p.xaxis.axis_label = 'Investment rate'
    p.yaxis.axis_label = 'k€'
    

    output_file("output/investment_tradeoff_continuous.html", title="Money invested.")
    show(column(p, spinner_year, row(spinner_saving, spinner_salary), 
                row(spinner_Fees, spinner_Div),
                row(spinner_Price, spinner_Capital)))



    
    
    