import java.awt.Color;
import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.text.DecimalFormat;
import java.text.SimpleDateFormat;
 
import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartUtilities;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.labels.StandardXYToolTipGenerator;
import org.jfree.chart.plot.XYPlot;
import org.jfree.chart.renderer.xy.XYItemRenderer;
import org.jfree.chart.renderer.xy.XYLineAndShapeRenderer;
import org.jfree.data.time.Hour;
import org.jfree.data.time.TimeSeries;
import org.jfree.data.time.TimeSeriesCollection;
import org.jfree.data.xy.XYDataset;
import org.jfree.ui.ApplicationFrame;
/**
 * A time series chart.
 */
public class PGMN_WaterLevel_Update extends ApplicationFrame {
 
    /**
     *
     */
    private static final long serialVersionUID = 1L;
    final static String waterlevel_fr = "Niveau d'eau";
    final static String waterlevel_en = "Water Level";
    /**
     * A demonstration application showing how to create a simple time series chart.
     *
     * @param title  the frame title.
     */
    public PGMN_WaterLevel_Update(final String title) {
        super(title);
        try{
            String [] stationList = {"W0000001-1", "W0000002-1", "W0000003-1", "W0000004-1", "W0000005-1", "W0000006-1", "W0000007-2", "W0000008-1", "W0000009-1", "W0000010-1", "W0000011-1", "W0000012-1", "W0000013-1", "W0000014-1", "W0000015-1", "W0000016-3", "W0000017-2", "W0000018-1", "W0000019-1", "W0000020-1", "W0000021-1", "W0000022-1", "W0000023-1", "W0000024-2", "W0000024-4", "W0000026-1", "W0000027-1", "W0000028-2", "W0000028-4", "W0000029-1", "W0000030-1", "W0000031-1", "W0000032-1", "W0000033-1", "W0000034-1", "W0000035-5", "W0000036-1", "W0000037-1", "W0000038-1", "W0000039-1", "W0000040-1", "W0000041-1", "W0000042-1", "W0000043-3", "W0000044-2", "W0000044-3", "W0000045-1", "W0000046-1", "W0000049-1", "W0000053-1", "W0000054-1", "W0000055-1", "W0000056-1", "W0000058-1", "W0000059-1", "W0000060-1", "W0000061-1", "W0000062-1", "W0000063-3", "W0000064-1", "W0000065-4", "W0000066-1", "W0000067-1", "W0000068-1", "W0000069-1", "W0000070-1", "W0000071-1", "W0000073-1", "W0000075-1", "W0000076-1", "W0000077-1", "W0000078-1", "W0000079-1", "W0000080-1", "W0000081-1", "W0000082-1", "W0000083-1", "W0000084-1", "W0000085-1", "W0000086-1", "W0000087-1", "W0000088-1", "W0000089-1", "W0000091-1", "W0000092-1", "W0000093-1", "W0000094-1", "W0000095-1", "W0000096-1", "W0000097-2", "W0000097-5", "W0000098-1", "W0000099-1", "W0000101-1", "W0000102-1", "W0000106-2", "W0000107-1", "W0000108-1", "W0000109-2", "W0000111-3", "W0000112-1", "W0000113-1", "W0000114-2", "W0000114-3", "W0000114-4", "W0000115-2", "W0000115-3", "W0000117-2", "W0000118-2", "W0000119-2", "W0000121-1", "W0000122-1", "W0000123-1", "W0000124-1", "W0000125-1", "W0000127-1", "W0000129-1", "W0000130-1", "W0000131-1", "W0000132-1", "W0000133-1", "W0000134-1", "W0000135-1", "W0000136-1", "W0000137-1", "W0000138-1", "W0000139-1", "W0000140-1", "W0000142-1", "W0000144-1", "W0000145-1", "W0000146-1", "W0000148-1", "W0000151-1", "W0000152-1", "W0000153-1", "W0000154-1", "W0000155-1", "W0000156-2", "W0000156-3", "W0000157-2", "W0000157-3", "W0000158-1", "W0000159-2", "W0000159-3", "W0000162-1", "W0000163-2", "W0000163-3", "W0000164-2", "W0000164-3", "W0000165-2", "W0000165-3", "W0000166-1", "W0000167-1", "W0000168-1", "W0000169-1", "W0000170-2", "W0000170-3", "W0000171-2", "W0000172-1", "W0000173-1", "W0000174-1", "W0000175-2", "W0000175-3", "W0000176-1", "W0000177-1", "W0000177-2", "W0000177-3", "W0000178-1", "W0000180-1", "W0000181-1", "W0000182-1", "W0000184-1", "W0000185-1", "W0000186-1", "W0000187-2", "W0000187-3", "W0000188-2", "W0000188-3", "W0000189-2", "W0000190-1", "W0000192-1", "W0000193-1", "W0000195-1", "W0000196-1", "W0000197-1", "W0000198-1", "W0000200-1", "W0000201-3", "W0000203-1", "W0000204-1", "W0000205-2", "W0000205-3", "W0000206-1", "W0000207-1", "W0000208-1", "W0000209-1", "W0000211-1", "W0000212-1", "W0000213-1", "W0000214-1", "W0000215-1", "W0000216-2", "W0000217-2", "W0000218-3", "W0000218-4", "W0000218-5", "W0000219-1", "W0000220-2", "W0000221-1", "W0000222-1", "W0000223-1", "W0000224-1", "W0000225-1", "W0000227-1", "W0000228-1", "W0000229-1", "W0000230-1", "W0000231-1", "W0000232-2", "W0000233-1", "W0000234-1", "W0000236-1", "W0000237-1", "W0000240-1", "W0000242-1", "W0000243-1", "W0000244-2", "W0000245-2", "W0000246-1", "W0000247-1", "W0000248-1", "W0000249-1", "W0000250-1", "W0000251-1", "W0000252-1", "W0000253-1", "W0000254-1", "W0000255-2", "W0000255-3", "W0000258-1", "W0000259-2", "W0000259-3", "W0000260-1", "W0000261-1", "W0000262-1", "W0000263-1", "W0000264-2", "W0000264-3", "W0000265-2", "W0000266-1", "W0000267-1", "W0000268-1", "W0000269-1", "W0000270-1", "W0000271-1", "W0000272-1", "W0000274-1", "W0000275-1", "W0000276-2", "W0000276-3", "W0000277-1", "W0000278-1", "W0000279-1", "W0000280-4", "W0000281-1", "W0000282-3", "W0000283-1", "W0000284-1", "W0000285-1", "W0000286-1", "W0000287-1", "W0000288-1", "W0000289-1", "W0000290-1", "W0000291-1", "W0000292-1", "W0000293-2", "W0000293-3", "W0000294-1", "W0000295-1", "W0000296-1", "W0000297-1", "W0000298-2", "W0000298-3", "W0000298-4", "W0000299-1", "W0000300-2", "W0000300-3", "W0000301-1", "W0000302-2", "W0000302-3", "W0000303-2", "W0000303-3", "W0000304-1", "W0000305-1", "W0000306-1", "W0000307-1", "W0000309-2", "W0000309-3", "W0000310-1", "W0000311-1", "W0000312-1", "W0000313-1", "W0000314-1", "W0000315-1", "W0000316-1", "W0000317-1", "W0000318-1", "W0000319-1", "W0000321-1", "W0000322-1", "W0000323-2", "W0000323-3", "W0000323-4", "W0000324-2", "W0000324-3", "W0000325-1", "W0000326-2", "W0000326-3", "W0000327-3", "W0000327-4", "W0000328-1", "W0000329-1", "W0000330-1", "W0000331-1", "W0000332-1", "W0000333-1", "W0000334-1", "W0000335-2", "W0000335-3", "W0000336-1", "W0000337-1", "W0000338-1", "W0000340-1", "W0000341-1", "W0000342-1", "W0000343-2", "W0000343-3", "W0000344-1", "W0000345-1", "W0000346-1", "W0000347-2", "W0000347-3", "W0000348-1", "W0000349-1", "W0000350-2", "W0000350-3", "W0000351-1", "W0000352-2", "W0000352-3", "W0000353-1", "W0000354-1", "W0000355-1", "W0000356-2", "W0000356-3", "W0000357-1", "W0000358-1", "W0000359-1", "W0000361-2", "W0000361-3", "W0000362-2", "W0000362-3", "W0000363-2", "W0000363-3", "W0000364-1", "W0000365-1", "W0000366-1", "W0000367-1", "W0000368-1", "W0000369-2", "W0000369-3", "W0000370-1", "W0000371-2", "W0000371-3", "W0000372-1", "W0000373-1", "W0000374-1", "W0000375-1", "W0000376-1", "W0000377-1", "W0000378-1", "W0000379-1", "W0000380-1", "W0000381-1", "W0000382-1", "W0000383-1", "W0000384-1", "W0000386-1", "W0000387-1", "W0000388-1", "W0000389-2", "W0000389-3", "W0000390-1", "W0000391-1", "W0000392-1", "W0000393-1", "W0000394-1", "W0000395-1", "W0000396-1", "W0000397-1", "W0000398-1", "W0000399-1", "W0000400-2", "W0000400-3", "W0000401-1", "W0000402-1", "W0000403-1", "W0000404-1", "W0000405-1", "W0000406-1", "W0000407-1", "W0000408-1", "W0000409-1", "W0000410-1", "W0000411-2", "W0000411-3", "W0000412-1", "W0000413-1", "W0000414-1", "W0000415-1", "W0000416-1", "W0000417-1", "W0000418-1", "W0000419-1", "W0000420-1", "W0000421-1", "W0000423-1", "W0000424-1", "W0000425-1", "W0000426-1", "W0000427-1", "W0000428-1", "W0000429-1", "W0000430-1", "W0000431-1", "W0000432-1", "W0000433-1", "W0000435-1", "W0000436-1", "W0000437-1", "W0000438-1", "W0000439-1", "W0000440-1", "W0000441-1", "W0000442-1", "W0000443-1", "W0000444-1", "W0000445-1", "W0000446-1", "W0000447-1", "W0000448-1", "W0000449-1", "W0000450-1", "W0000451-1", "W0000452-1", "W0000453-1", "W0000454-1", "W0000455-1", "W0000456-1", "W0000457-1", "W0000458-1", "W0000459-1", "W0000460-1", "W0000461-1", "W0000462-1", "W0000463-1", "W0000464-1", "W0000465-1", "W0000466-1", "W0000467-1", "W0000468-1", "W0000469-1", "W0000470-1", "W0000471-1", "W0000473-1", "W0000474-1", "W0000475-1", "W0000476-1", "W0000477-1", "W0000478-1", "W0000479-1", "W0000480-1", "W0000481-1", "W0000482-1", "W0000486-1"};
            //String [] stationList = {"W0000008-1"};
            /*FileInputStream fstream = new FileInputStream("Y:\\PGMN\\WaterLevel\\csv\\1a.txt");
            DataInputStream in = new DataInputStream(fstream);
            BufferedReader br = new BufferedReader(new InputStreamReader(in));
            String strLine;
            int i = 0;
            while ((strLine = br.readLine()) != null)   {
                  if(strLine.length() != 53){
                      continue;
                  }
                  String wellId = strLine.substring(39, 49);
                  */
            for (int i = 0; i < stationList.length; i++) {
                String wellId = stationList[i];
                System.out.println(wellId);
                String [] languageList = {"EN", "FR"};
                for (int j = 0; j < languageList.length; j++) {
                    String lang = languageList[j];
                    final XYDataset dataset = createDataset(wellId, lang);
                    final JFreeChart chart = createChart(dataset, wellId, lang);
                    XYPlot xyplot = (XYPlot)chart.getPlot();
                    XYLineAndShapeRenderer renderer = (XYLineAndShapeRenderer)xyplot.getRenderer();
                    renderer.setSeriesPaint(0, Color.blue);
                    try {
                        ChartUtilities.saveChartAsPNG(new File("Y:\\PGMN\\WaterLevel\\png\\" + lang + "\\" + wellId + ".png"), chart, 400, 300);
                    }
                    catch (Exception e) {
                        System.err.println("PGMN_WaterLevel_Update: " + e.getMessage());
                    }
                }
 
            /*
            lang = "FR";
            final XYDataset dataset_fr = createDataset(wellId, lang);
            final JFreeChart chart_fr = createChart(dataset_fr, wellId, lang);
            XYPlot xyplot_fr = (XYPlot)chart_fr.getPlot();
            XYLineAndShapeRenderer renderer_fr = (XYLineAndShapeRenderer)xyplot_fr.getRenderer();
            renderer_fr.setSeriesPaint(0, Color.blue);
            try {
                ChartUtilities.saveChartAsPNG(new File("Y:\\PGMN\\WaterLevel\\png\\" + lang + "\\" + wellId + ".png"), chart_fr, 400, 300);
                }
                catch (Exception e) {
                    System.err.println(e.getMessage());
                }*/
                //i++;
              }
              //Close the input stream
              //in.close();
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
        String waterlevel = "";
        if(lang.equals("EN")){
            waterlevel = waterlevel_en;
        }else{
            waterlevel = waterlevel_fr;
        }
        TimeSeries t1 = new TimeSeries(waterlevel + " (m.a.s.l.)");
        //System.out.println (t1.getMaximumItemCount());
        Hour begin = new Hour(1, 1, 1, 2001);
        Hour end = new Hour(23, 31, 12, 2010);
        //System.out.println(begin);
        String endStr = end.toString();
        //System.out.println(endStr);
        String str = begin.toString();
        for(Hour h1 = begin;  !str.equals(endStr) ; h1 = (Hour) h1.next()){
            t1.addOrUpdate(h1, new Double(Double.NaN));
            str = h1.toString();
        }
        try {
                  // Open the file that is the first
                  // command line parameter
                  FileInputStream fstream = new FileInputStream("Y:\\PGMN\\WaterLevel\\csv\\" + WellID + ".csv");
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
                      String [] temp1 = (temp[1]).split(" ");  //6/10/2009 21:00:00
                      String [] temp2 = (temp1[0]).split("/");  //6/10/2009 21:00:00
                      int day = Integer.parseInt(temp2[2]);
                      int month = Integer.parseInt(temp2[1]);
                      int year = Integer.parseInt(temp2[0]);
                      //System.out.println (i);
 
                      String [] temp3 = (temp1[1]).split(":");  //6/10/2009 21:00:00
                      int hour = Integer.parseInt(temp3[0]);
                      int minute = Integer.parseInt(temp3[1]);
                      int second = Integer.parseInt(temp3[2]);
                      //Second s = new Second(second, minute, hour, day, month, year);
                      Hour h = new Hour(hour, day, month, year);
                      Double d = new Double(Double.NaN);
 
                      if (temp.length > 2){
                              d = Double.parseDouble(temp[2]);// - depth;
                              count ++;
                      }
                      t1.addOrUpdate(h, d);
                     }
                    i = i + 1;
                  }
                  in.close();
 
        }
        catch (Exception e) {
            System.err.println("createEURTimeSeries : " + e.getMessage());
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
        String waterlevel = "";
        if(lang.equals("EN")){
            waterlevel = waterlevel_en;
        }else{
            waterlevel = waterlevel_fr;
        }
        final JFreeChart chart = ChartFactory.createTimeSeriesChart(
                waterlevel + " (" + WellID + ")",
            "Date",
            waterlevel + " (m.a.s.l.)",
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
 
        PGMN_WaterLevel_Update demo = new PGMN_WaterLevel_Update("Time Series Demo 8");
        /*demo.pack();
        RefineryUtilities.centerFrameOnScreen(demo);
        demo.setVisible(true);*/
 
    }
 
}