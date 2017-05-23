package com.drexelchatbot;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.log4j.Logger;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.twilio.Twilio;
import com.twilio.http.TwilioRestClient;
import com.twilio.rest.api.v2010.account.Message;
import com.twilio.type.PhoneNumber;

@RestController
public class ApplicationController {

	public static final String ACCOUNT_SID = "ACd4b939c41705228c35abfaf56956e9a3";
	public static final String AUTH_TOKEN = "d4a1f04caafb661295ae646e2a1471e8";

	Logger log = Logger.getLogger(ApplicationController.class);

	@RequestMapping(value = "/chatbot/api", method = RequestMethod.GET)
	public QueryResponse response(@RequestParam(value = "query", defaultValue = "") String query,
			HttpServletRequest request) {
		log.info("Responding to query: '" + query + "'" + " from remote IP " + request.getRemoteAddr());

		log.info("Processing query: '" + query + "'" + " from remote IP " + request.getRemoteAddr());

		Process cmdProc = null;
		String line = null;
		String ret = "";
		try {
			cmdProc = Runtime.getRuntime()
					.exec(new String[] { "python3", "./../chatbot/main.py", "\"" + query + "\"", "2>/dev/null" });

			BufferedReader stdoutReader = new BufferedReader(new InputStreamReader(cmdProc.getInputStream()));
			while ((line = stdoutReader.readLine()) != null) {
				// process standard output here
				System.out.println(line);
				if (line != null) {
					ret += line;
				}
			}

			BufferedReader stderrReader = new BufferedReader(new InputStreamReader(cmdProc.getErrorStream()));
			while ((line = stderrReader.readLine()) != null) {
				// process standard error here
				// System.err.println(line);
			}
			cmdProc.waitFor();
			int retValue = cmdProc.exitValue();
			cmdProc.destroy();
		} catch (IOException | InterruptedException e) {

			e.printStackTrace();
		}

		log.info("Returning for query: '" + query + "'" + " from remote IP " + request.getRemoteAddr());
		if (ret.equals("")) {
			ret = "I'm sorry, I was unable to porcess your request.";
		}
		return new QueryResponse(ret);
	}

	@RequestMapping(value = "/chatbot/api", method = RequestMethod.POST)
	public void sms(HttpServletRequest request, HttpServletResponse response) {
		Twilio.init(ACCOUNT_SID, AUTH_TOKEN);
		String query = request.getParameter("Body");
		String sender = request.getParameter("From");
		String rec = request.getParameter("To");
		System.out.println("Sender: " + sender + "\tRec: " + rec + "\tQuery: " +query);
		if(query != null && !"".equals(query)){
			Process cmdProc = null;
			String line = null;
			String ret = "";
			try {
				cmdProc = Runtime.getRuntime()
						.exec(new String[] { "python3", "./../chatbot/main.py", "\"" + query + "\"", "2>/dev/null" });

				BufferedReader stdoutReader = new BufferedReader(new InputStreamReader(cmdProc.getInputStream()));
				while ((line = stdoutReader.readLine()) != null) {
					// process standard output here
					System.out.println(line);
					if (line != null) {
						ret += line;
					}
				}

				BufferedReader stderrReader = new BufferedReader(new InputStreamReader(cmdProc.getErrorStream()));
				while ((line = stderrReader.readLine()) != null) {
					// process standard error here
					// System.err.println(line);
				}
				cmdProc.waitFor();
				int retValue = cmdProc.exitValue();
				cmdProc.destroy();
				Message message = Message
		                .creator(new PhoneNumber(sender),  // to
		                         new PhoneNumber(rec),  // from
		                         ret).create();
				
			} catch (IOException | InterruptedException e) {

				e.printStackTrace();
			}
		}
	}

}
