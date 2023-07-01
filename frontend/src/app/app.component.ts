import {Component} from '@angular/core';
import {HttpClient} from "@angular/common/http";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  code = "int test() {\n    return 42;\n}\n"
  result = "; no result available"

  loading = false;

  constructor(private http: HttpClient) {
  }

  doCompile() {
    this.loading = true;
    this.http.post<any>("/api/compile", {code: this.code}).subscribe(result => {
      this.result = result.asm;
      this.loading = false;
    }, error => {
      this.result = "; error";
      this.loading = false;
    });
  }

  public onCodeChangew(event: Event) {
    this.code = (event.target as any).value;
  }
}
