import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";

interface CompileRequest {
  code: string;
  compiler: string;
}

interface CompileResponse {
  asm: string;
}

interface CompilerSummary {
  id: string;
  name: string;
  target: string;
  available: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class CompilerService {

  constructor(private http: HttpClient) {
  }

  public compile(request: CompileRequest): Observable<CompileResponse> {
    return this.http.post<CompileResponse>("/api/compile", request);
  }

  public listCompilers(): Observable<CompilerSummary[]> {
    return this.http.get<CompilerSummary[]>("/api/compiler");
  }
}
