import java.awt.Color;
import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.text.DateFormat;
import java.text.DecimalFormat;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;
 
import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartUtilities;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.labels.StandardXYToolTipGenerator;
import org.jfree.chart.plot.XYPlot;
import org.jfree.chart.renderer.xy.XYItemRenderer;
import org.jfree.chart.renderer.xy.XYLineAndShapeRenderer;
import org.jfree.data.time.Hour;
import org.jfree.data.time.Second;
import org.jfree.data.time.TimeSeries;
import org.jfree.data.time.TimeSeriesCollection;
import org.jfree.data.xy.XYDataset;
import org.jfree.ui.ApplicationFrame;
/**
 * A time series chart.
 */
public class PGMN_Precipitation extends ApplicationFrame {
    final static String precipitation_fr = "Précipitation";
    final static String precipitation_en = "Precipitation";
    final static String site_id_en = "Site ID";
    final static String site_id_fr = "Numéro du site";
    /**
     * A demonstration application showing how to create a simple time series chart.
     *
     * @param title  the frame title.
     */
    public PGMN_Precipitation(final String title) {
        super(title);
        try{
              // Open the file that is the first 
              // command line parameter
              FileInputStream fstream = new FileInputStream("Y:\\PGMN\\Precipitation\\1.txt");
              // Get the object of DataInputStream
              DataInputStream in = new DataInputStream(fstream);
              BufferedReader br = new BufferedReader(new InputStreamReader(in));
              String strLine;
              //Read File Line By Line
              int i = 0;
              while ((strLine = br.readLine()) != null)   {
                  //System.out.println(strLine.length());
                  if((strLine.length() < 45)||(strLine.length() > 46)){
                      continue;
                  }
                  if(!strLine.contains("csv")){
                      continue;
                  }
 
                  String wellId = strLine.substring(39, strLine.length()-4);
                  System.out.println(wellId);
                //Double depth = (Double)hm.get(wellId);
                String lang = "EN";
                final XYDataset dataset = createDataset(wellId, lang);
                final JFreeChart chart = createChart(dataset, wellId, lang);
                XYPlot xyplot = (XYPlot)chart.getPlot();
                XYLineAndShapeRenderer renderer = (XYLineAndShapeRenderer)xyplot.getRenderer();
                renderer.setSeriesPaint(0, Color.blue);
                try {
                    ChartUtilities.saveChartAsPNG(new File("Y:\\PGMN\\Precipitation\\" + lang + "\\" + wellId + ".png"), chart, 400, 300);
                }
                catch (Exception e) {
                    System.err.println(e.getMessage());
                }
                 
                lang = "FR";
                final XYDataset dataset_fr = createDataset(wellId, lang);
                final JFreeChart chart_fr = createChart(dataset_fr, wellId, lang);
                XYPlot xyplot_fr = (XYPlot)chart_fr.getPlot();
                XYLineAndShapeRenderer renderer_fr = (XYLineAndShapeRenderer)xyplot_fr.getRenderer();
                renderer_fr.setSeriesPaint(0, Color.blue);
                try {
                    ChartUtilities.saveChartAsPNG(new File("Y:\\PGMN\\Precipitation\\" + lang + "\\" + wellId + ".png"), chart_fr, 400, 300);
                }
                catch (Exception e) {
                    System.err.println(e.getMessage());
                }
                i++;
              }
              //Close the input stream
              in.close();
                }catch (Exception e){//Catch exception if any
              System.err.println("Error: " + e.getMessage());
              }
    }
    /**
     * Returns a time series of the daily EUR/GBP exchange rates in 2001 (to date), for use in
     * the JFreeChart demonstration application.
     * <P>
     * You wouldn't normally create a time series in this way.  Typically, values would
     * be read from a database.
     *
     * @return a time series.
     *
     */
    private TimeSeries createEURTimeSeries(String WellID, String lang) {
        int count = 0;
        String precipitation = "";
        if(lang.equals("EN")){
            precipitation = precipitation_en;
        }else{
            precipitation = precipitation_fr;
        }
        TimeSeries t1 = new TimeSeries(precipitation + " (mm)");
        //System.out.println (t1.getMaximumItemCount());        
        Hour begin = new Hour( 1, 1, 1, 2005);
        Hour end = new Hour(23, 31, 12, 2012);
        String endStr = end.toString();
        String str = begin.toString();
         
        for(Hour h1 = begin;  !str.equals(endStr) ; h1 = (Hour) h1.next()){
            Second s = new Second(0, 0, h1.getHour(), h1.getDayOfMonth(), h1.getMonth(), h1.getYear());
            t1.addOrUpdate(s, new Double(Double.NaN));              
            str = h1.toString();
        }
  
        try {
                  // Open the file that is the first 
                  // command line parameter
                  FileInputStream fstream = new FileInputStream("Y:\\PGMN\\Precipitation\\" + WellID + ".csv");
                  // Get the object of DataInputStream
                  DataInputStream in = new DataInputStream(fstream);
                  BufferedReader br = new BufferedReader(new InputStreamReader(in));
                  String strLine;
                  //Read File Line By Line
                  int i = 0;
                  while ((strLine = br.readLine()) != null)   {
                     if(i>0){  
                      String [] temp = strLine.split(",");
                      //System.out.println (i);
                      String [] dateTimeAM = (temp[2]).split(" ");  //08/20/2009 10:35:00 AM
 
                      String [] dates = (dateTimeAM[0]).split("/");  //6/10/2009
                      int month = Integer.parseInt(dates[0]);
                      int day = Integer.parseInt(dates[1]);
                      int year = Integer.parseInt(dates[2]);
                      //System.out.println (i);
                      int hour = 0;
                      int minute = 0;
                      int second = 0;                     
                      if (dateTimeAM.length > 1) {
                          String [] temp3 = (dateTimeAM[1]).split(":");  //10:35:00
                          hour = Integer.parseInt(temp3[0]);
                          minute = Integer.parseInt(temp3[1]);
                          second = Integer.parseInt(temp3[2]);
                          //08/20/2009 10:35:00 AM
                          if ((dateTimeAM[2]).equals("PM")) {
                              if (hour < 12) {
                                  hour = hour + 12;
                              }
                          }
                          if ((dateTimeAM[2]).equals("AM") && (hour == 12)) {
                                  hour = 0;
                          }
                      }
                      Second s = new Second(second, minute, hour, day, month, year);
                      //System.out.println(strLine);
                      //System.out.println(year + ", " + month + ", " + day + ", " + hour + ", " + minute + ", " + second);
                      //Hour h = new Hour(hour, day, month, year);
                      Double d = new Double(Double.NaN);
                      //System.out.println(temp[2]);
                      if (temp.length > 2){
                            d = Double.parseDouble(temp[3]);// - depth;
                            count ++;
                      }
                      t1.addOrUpdate(s, d);
                     }
                    i = i + 1;
                  }
                  in.close();
  
        }
        catch (Exception e) {
            System.err.println(e.getMessage());
        }
         
        return t1;
    }
     
    /**
     * Creates a sample dataset.
     * 
     * @return a sample dataset.
     */
    private XYDataset createDataset(String WellID, String lang) {
        final TimeSeries eur = createEURTimeSeries(WellID, lang);
        final TimeSeriesCollection dataset = new TimeSeriesCollection();
        dataset.addSeries(eur);
        return dataset;
    }
     
    /**
     * Creates a chart.
     * 
     * @param dataset  the dataset.
     * 
     * @return a chart.
     */
    private JFreeChart createChart(final XYDataset dataset, String WellID, String lang) {
        String precipitation = "";
        if(lang.equals("EN")){
            precipitation = precipitation_en;
        }else{
            precipitation = precipitation_fr;
        }
        String site_id = "";
        if(lang.equals("EN")){
            site_id = site_id_en;
        }else{
            site_id = site_id_fr;
        }
        final JFreeChart chart = ChartFactory.createTimeSeriesChart(
                precipitation + " (" + site_id +": " + WellID + ")", 
            "Date", 
            precipitation + " (mm)",
            dataset, 
            true, 
            true, 
            false
        );
        final XYItemRenderer renderer = chart.getXYPlot().getRenderer();
        final StandardXYToolTipGenerator g = new StandardXYToolTipGenerator(
            StandardXYToolTipGenerator.DEFAULT_TOOL_TIP_FORMAT,
            new SimpleDateFormat("d-MMM-yyyy"), new DecimalFormat("0.00")
        );
        renderer.setToolTipGenerator(g);
        return chart;
    }
     
    // ****************************************************************************
    // * JFREECHART DEVELOPER GUIDE                                               *
    // * The JFreeChart Developer Guide, written by David Gilbert, is available   *
    // * to purchase from Object Refinery Limited:                                *
    // *                                                                          *
    // * http://www.object-refinery.com/jfreechart/guide.html                     *
    // *                                                                          *
    // * Sales are used to provide funding for the JFreeChart project - please    * 
    // * support us so that we can continue developing free software.             *
    // ****************************************************************************
     
    /**
     * Starting point for the demonstration application.
     *
     * @param args  ignored.
     */
    public static void main(final String[] args) {
 
        final PGMN_Precipitation demo = new PGMN_Precipitation("Time Series Demo 8");
        /*demo.pack();
        RefineryUtilities.centerFrameOnScreen(demo);
        demo.setVisible(true);*/
 
    }
 
}