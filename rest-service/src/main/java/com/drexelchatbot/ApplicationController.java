package com.drexelchatbot;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

import javax.servlet.http.HttpServletRequest;

import org.apache.log4j.Logger;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ApplicationController {
	Logger log = Logger.getLogger(ApplicationController.class);

	@RequestMapping(value = "/chatbot/api", method = RequestMethod.GET)
	public QueryResponse response(@RequestParam(value = "query", defaultValue = "") String query,
			HttpServletRequest request) {
		log.info("Responding to query: '" + query + "'" + " from remote IP " + request.getRemoteAddr());

		log.info("Processing query: '" + query + "'" + " from remote IP " + request.getRemoteAddr());

		Process cmdProc;
		try {
			cmdProc = Runtime.getRuntime().exec(new String[] { "python", "./../chatbot/main.py", query});

			BufferedReader stdoutReader = new BufferedReader(new InputStreamReader(cmdProc.getInputStream()));
			String line;
			while ((line = stdoutReader.readLine()) != null) {
				// process standard output here
				System.out.println(line);
			}

			BufferedReader stderrReader = new BufferedReader(new InputStreamReader(cmdProc.getErrorStream()));
			while ((line = stderrReader.readLine()) != null) {
				// process standard error here
				System.out.println(line);
			}

			int retValue = cmdProc.exitValue();
		} catch (IOException e) {
			e.printStackTrace();
		}

		log.info("Returning for query: '" + query + "'" + " from remote IP " + request.getRemoteAddr());

		return new QueryResponse(String.format("Responding to query: '" + query + "'"));
	}

}
