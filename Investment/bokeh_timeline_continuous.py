"""
Script for temporal TS
To see how:

- Capital 
- Reimbursment 
- Dividend

improve over a 25 year period.
This is without reinvesting dividends !
"""

from bokeh.plotting  import ColumnDataSource, figure, output_file, show
from bokeh.models    import HoverTool, CustomJS
from bokeh.layouts   import column, row
from bokeh.events import DoubleTap#DocumentReady
from bokeh.models import Spinner, Span
import numpy as np

if __name__ == "__main__":
    
    #TODO
    
    
    
    alpha=100
    saving=10
    salary=10
    fees = 3
    divs = 5
    capital=100
    price = 200
    
    k_split = 50
    x_range = np.linspace(0, 25, 25*k_split)
    
    
    def savings(timing):
        
        np_all = np.zeros(len(timing))
        
        ai = alpha/100
        fx = fees/100
        dv = divs/100
        
        left_to_pay = max(0, price - capital * ai)
        invested0   = capital - (price - left_to_pay)
        t1 = left_to_pay / salary
        
        tot_fees = left_to_pay / 2 * (t1+1) * fx
        fee_per_year = tot_fees / t1
        
        r1 = np.exp(np.log(1 + divs/100) / k_split)
        c0 = invested0
        for i, time in enumerate(timing[:-1]):
            if (time < t1):                
                c0 = c0 * r1 + (saving - fee_per_year)/k_split
                np_all[i+1] = c0
            
            else:
                c0 = c0 * r1 + (saving + salary)/k_split
                np_all[i+1] = c0

    
        return np_all

    y_capital = savings(x_range)
    
    source   = ColumnDataSource(data=dict(x=x_range, y=y_capital))
    
    t1 = (price - alpha*capital/100) / salary
    my_span = Span(location=t1,
                            dimension='height', line_color='gray',
                            line_dash='dashed', line_width=3)
    
    
    W = 120
    
    spinner_alpha   = Spinner(title="Part of capital invested", low=0, high=100, step=0.5, value=alpha, width=W)
    spinner_saving  = Spinner(title="Saving per year", low=0,  high=50, step=0.1, value=saving, width=W)
    spinner_salary  = Spinner(title="Salary per year", low=0,  high=50, step=0.1, value=salary, width=W)
    spinner_Fees    = Spinner(title="Loan fee (%)", low=0,  high=100, step=0.1, value=fees, width=W)
    spinner_Div     = Spinner(title="Dividend rate (%)", low=0,  high=100, step=0.1, value=divs, width=W)
    spinner_Capital = Spinner(title="Capital at t=0", low=0,  high=1000, step=1, value=capital, width=W)
    spinner_Price   = Spinner(title="House price", low=0,  high=2000, step=1, value=price, width=W)
    
    

    callback = CustomJS(args=dict(source=source,
        sp_alpha=spinner_alpha,
        sp_salary=spinner_salary,
        sp_saving=spinner_saving,
        sp_fees=spinner_Fees,
        sp_divs=spinner_Div,
        sp_capital=spinner_Capital,
        sp_price=spinner_Price,
        span=my_span,
        k_split=k_split
        ),
                        code="""
        
        const data = source.data;
        
        
        const alpha = sp_alpha.value / 100; // Percentage of the capital invested for buying
        
        const capital0 = sp_capital.value; // initial capital
        const price = sp_price.value; // cost of the house
        
        const salary = sp_salary.value;
        const saving = sp_saving.value;
        
        const fees = sp_fees.value / 100;
        const divs = sp_divs.value / 100;


        // How long does it take to reimburse ?
        var left_to_pay = Math.max(0, price - capital0 * alpha);
        var invested0   = capital0 - (price - left_to_pay);  // Capital left for dividend
        var t1 = left_to_pay / salary; // Time needed to reimburse the loan
        
        var tot_fees = left_to_pay / 2 * (t1+1) * fees; // Total amount of fees
        var fee_per_year = tot_fees / t1; // interest fees per year
        
        span.location = t1;
        var r1 = Math.exp(Math.log(1+divs)/k_split)
        
        var c0 = invested0;
        
        for (var i=0; i < data.x.length; i++) {
            var time = data.x[i]; // time in years
            if (time < t1) {
                c0 = c0 * r1 + (saving - fee_per_year)/k_split                
                data.y[i]     = c0
            
            } else {
                c0 = c0 * r1 + (saving + salary) / k_split                
                data.y[i]     = c0
            }

        }

        source.change.emit();
        """)
    
    spinner_alpha.js_on_change('value', callback)
    spinner_saving.js_on_change('value', callback)
    spinner_salary.js_on_change('value', callback)
    spinner_Fees.js_on_change('value', callback)
    spinner_Div.js_on_change('value', callback)
    spinner_Capital.js_on_change('value', callback)
    spinner_Price.js_on_change('value', callback)
    
    #spinner_alpha.on_event("DocumentReady", callback)
    
    p = figure(plot_width=1000, plot_height=700,
            x_range=[-0.05, 26],
            #y_range=[0, 105],
            tools="pan,wheel_zoom,reset,save",
           title="Capital after investment.")

    # Plot circles. Define name for the item
    p.line('x', 'y', name="lines", source=source, line_width=3, line_alpha=0.7, legend_label="Div + Cap")
    p.add_layout(my_span)

    p.legend.location = "top_left"
    p.legend.title = "Legend"
    
    hover = HoverTool(tooltips=[("Year", '@x'), 
                                ("Total", "@y"),
                               ])
    p.add_tools(hover)


    p.xaxis.axis_label = 'Time'
    p.yaxis.axis_label = 'k€'
    
    

    output_file("output/investment_temporal_continuous.html", title="Money invested.")
    show(column(p, spinner_alpha, row(spinner_saving, spinner_salary), 
                row(spinner_Fees, spinner_Div),
                row(spinner_Price, spinner_Capital)))



    
    
    